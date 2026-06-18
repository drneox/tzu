#Requires -Version 5.1
<#
.SYNOPSIS
    TZU - Threat Zero Utility startup script for Windows.
.DESCRIPTION
    Windows equivalent of start.sh. Requires Docker Desktop with WSL2 backend.
    Usage: .\start.ps1
#>

Write-Host ""
Write-Host "============================================================"
Write-Host "             TZU - Threat Zero Utility                     "
Write-Host "        Security Risk Assessment Platform                  "
Write-Host "             GitHub: drneox/tzu                            "
Write-Host "============================================================"
Write-Host ""

# Verify Docker is available
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Docker is not installed or not in PATH." -ForegroundColor Red
    Write-Host "       Install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Detect Docker Compose (V2 plugin preferred over legacy V1)
docker compose version 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Using: docker compose (V2)" -ForegroundColor Cyan
} elseif (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    Write-Host "WARNING: docker compose V2 not found, falling back to docker-compose V1." -ForegroundColor Yellow
} else {
    Write-Host "ERROR: Docker Compose is not installed." -ForegroundColor Red
    exit 1
}

function Invoke-Compose {
    param([string[]]$CmdArgs)
    docker compose version 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        & docker compose @CmdArgs
    } else {
        & docker-compose @CmdArgs
    }
}

Write-Host "Starting TZU with Docker..." -ForegroundColor Cyan

# Stop previous containers (keep volumes)
Push-Location docker
Invoke-Compose "down"
Pop-Location

# Build and start all services
Write-Host "Building and starting services..." -ForegroundColor Cyan
Push-Location docker
Invoke-Compose @("up", "-d", "--build")
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to start containers." -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

# Wait for all containers to reach running state
function Wait-Containers {
    $maxAttempts = 30
    Write-Host "Waiting for containers to start..."

    for ($i = 1; $i -le $maxAttempts; $i++) {
        Push-Location docker
        # Use -a so exited/crashed containers are listed, not silently hidden
        $psOutput = Invoke-Compose @("ps", "-a", "--format", "{{.Service}} {{.Status}}") 2>$null
        Pop-Location

        $services   = @("postgresql", "backend", "frontend", "nginx")
        $allRunning = $true
        $failed     = @()

        foreach ($svc in $services) {
            $line = ($psOutput | Select-String -Pattern "^$svc\b")
            if (-not $line) {
                $allRunning = $false
                $failed += "$svc(not_found)"
            } elseif ($line -match "Exit|exited|Restarting|restart") {
                $allRunning = $false
                $failed += "$svc(crashed -- check: cd docker; docker compose logs $svc)"
            } elseif ($line -notmatch "Up|running|healthy") {
                $allRunning = $false
                $failed += "$svc(starting)"
            }
        }

        if ($allRunning) {
            Write-Host "All containers are running." -ForegroundColor Green
            return $true
        }

        # Abort immediately if a container crashed (retrying won't help)
        $crashed = $failed | Where-Object { $_ -match "crashed" }
        if ($crashed) {
            Write-Host "ERROR: One or more containers crashed:" -ForegroundColor Red
            $crashed | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
            return $false
        }

        if ($i -eq $maxAttempts) {
            Write-Host "ERROR: Container validation failed after $maxAttempts attempts." -ForegroundColor Red
            Write-Host "       Failed: $($failed -join ', ')" -ForegroundColor Red
            return $false
        }

        Write-Host "  Attempt $i/$maxAttempts - waiting... ($($failed -join ', '))"
        Start-Sleep -Seconds 5
    }
    return $false
}

if (-not (Wait-Containers)) {
    Write-Host "TIP: Run 'cd docker; docker compose logs' to diagnose." -ForegroundColor Yellow
    exit 1
}

# Wait for backend to finish initializing
function Wait-BackendReady {
    $maxAttempts = 20
    Write-Host "Waiting for backend initialization..."

    for ($i = 1; $i -le $maxAttempts; $i++) {
        Push-Location docker
        $logs = Invoke-Compose @("logs", "backend") 2>&1
        Pop-Location

        $uvicornReady = $logs | Select-String "Uvicorn running on"
        $startupDone  = $logs | Select-String "Application startup complete"

        if ($uvicornReady -and $startupDone) {
            Write-Host "Backend initialization completed." -ForegroundColor Green
            Start-Sleep -Seconds 3
            return
        }

        if ($i -eq $maxAttempts) {
            Write-Host "WARNING: Backend init timed out -- proceeding anyway." -ForegroundColor Yellow
            return
        }

        Write-Host "  Attempt $i/$maxAttempts - waiting for backend..."
        Start-Sleep -Seconds 3
    }
}

Wait-BackendReady

# Capture credentials from backend logs
Push-Location docker
$backendLogs = Invoke-Compose @("logs", "backend") 2>&1
Pop-Location

$passwordLine = $backendLogs | Select-String "Password:" | Select-Object -Last 1
$createdLine  = $backendLogs | Select-String "DEFAULT USER CREDENTIALS CREATED"

$password = ""
if ($passwordLine) {
    $password = ($passwordLine.Line -replace ".*Password:\s*", "").Trim()
}

Write-Host ""
Write-Host "============================================================"
Write-Host "                   TZU IS RUNNING!"
Write-Host "============================================================"
Write-Host "  Application : http://localhost:3434"
Write-Host "  API Docs    : http://localhost:3434/api/docs"
Write-Host ""
Write-Host "  Username: admin"

if ($createdLine -and $password) {
    Write-Host "  Password: $password" -ForegroundColor Green
    Write-Host "  (auto-generated -- save it now)"
} else {
    Write-Host "  Password: [Hidden] -- run to retrieve:"
    Write-Host "    docker compose -f docker/docker-compose.yml exec backend python show_credentials.py"
}

Write-Host ""
Write-Host "  To stop : docker compose -f docker/docker-compose.yml down"
Write-Host "  Project : https://github.com/drneox/tzu"
Write-Host "============================================================"
Write-Host ""
