# API endpoints for TZU application
import os
import json
from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException, Depends, UploadFile, Body, status, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from jose import JWTError, jwt

# Configure timezone from environment variable
# Set timezone if TZ environment variable is set
if 'TZ' in os.environ:
    try:
        # Set the timezone for the application
        timezone_name = os.environ['TZ']
        os.environ['TZ'] = timezone_name
        print(f"🌍 Timezone set to: {timezone_name}")
    except Exception as e:
        print(f"⚠️ Warning: Could not set timezone {os.environ['TZ']}: {e}")

# Local imports
import models
import schemas
import crud
import database
import utils
import init_db
import control_tags
from tzu_ai import clientAI
from utils import save_image
from stride_validator import normalize_stride_category, get_valid_stride_categories

# Environment-based configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Configure documentation based on environment
docs_url = "/docs" if ENVIRONMENT == "development" else None
redoc_url = "/redoc" if ENVIRONMENT == "development" else None
openapi_url = "/openapi.json" if ENVIRONMENT == "development" else None

app = FastAPI(
    title="TZU - Threat Zero Utility API",
    description="""
    API for threat analysis and security risk management.
    
    ## Authentication
    Most endpoints require JWT authentication. Use the `/auth/login` endpoint to get a token.
    
    ## Security
    - All endpoints are protected with authentication
    - Implements rate limiting on sensitive endpoints
    - Strict input data validation
    
    ## Source Code
    This project is open source: [GitHub](https://github.com/drneox/tzu)
    """,
    version="1.0.0",
    contact={
        "name": "TZU Project",
        "url": "https://github.com/drneox/tzu",
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/drneox/tzu/blob/main/LICENSE",
    },
    # Configure documentation URLs based on environment
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)
origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Static files are now served by nginx
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/diagrams", StaticFiles(directory="diagrams"), name="diagrams")

# Endpoint to check database status
@app.get("/health")
async def health_check():
    """
    Endpoint to check application and database status
    """
    try:
        # Simple check to ensure the API is running
        return {"status": "ok", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to get database in each request
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="tzu-client")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Function to get active user
async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Batch endpoint to update risk values for multiple threats at once
class ThreatRiskUpdate(BaseModel):
    threat_id: str
    risk: dict


@app.get("/information_systems/{information_system_id}/threats", response_model=list[schemas.Threat])
async def get_threats_by_system(
    information_system_id: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        system_uuid = UUID(information_system_id)
    except Exception:
        raise HTTPException(status_code=400, detail="The system id is not a valid UUID")
    
    threats = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.information_system_id == system_uuid).all()
    return threats

@app.get("/threat/{threat_id}", response_model=schemas.Threat)
async def get_threat(
    threat_id: str = Path(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        uuid_id = UUID(threat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="The id is not a valid UUID")
    
    threat = db.query(models.Threat).filter(models.Threat.id == uuid_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

@app.get("/report", response_model=list[schemas.ThreatWithSystem])
async def get_threats_report(
    skip: int = 0,
    limit: int = 1000,
    standards: str = None,  # List of comma-separated standards: "ASVS,MASVS,NIST"
    system_id: str = None,  # Information system ID
    risk_level: str = None,  # Risk level: "LOW", "MEDIUM", "HIGH", "CRITICAL"
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Gets a report of all threats with optional filters"""
    
    # Process filtering parameters
    standards_list = []
    if standards:
        standards_list = [s.strip().upper() for s in standards.split(',') if s.strip()]
    
    threats = crud.get_all_threats(
        db, 
        skip=skip, 
        limit=limit,
        standards=standards_list,
        system_id=system_id,
        risk_level=risk_level.upper() if risk_level else None
    )
    return threats

@app.delete("/threat/{threat_id}")
async def delete_threat(
    threat_id: str = Path(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        uuid_id = UUID(threat_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="The id is not a valid UUID")
    
    threat = db.query(models.Threat).filter(models.Threat.id == uuid_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    db.delete(threat)
    db.commit()
    return {"message": "Threat deleted successfully", "status": "success", "id": str(uuid_id)}


# Endpoint to update risk values for a threat
@app.put("/threat/{threat_id}/risk", response_model=schemas.Threat)
async def update_threat_risk(
    threat_id: str,
    risk: dict = Body(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated_threat = crud.update_threat_risk(db, threat_id, risk)
    if not updated_threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return updated_threat

@app.post("/information_systems/{information_system_id}/threats", response_model=schemas.Threat)
async def create_threat_for_system(
    information_system_id: str,
    threat_data: dict = Body(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        system_uuid = UUID(information_system_id)
    except Exception:
        raise HTTPException(status_code=400, detail="The system id is not a valid UUID")
    
    # Verify that system exists
    system = db.query(models.InformationSystem).filter(models.InformationSystem.id == system_uuid).first()
    if not system:
        raise HTTPException(status_code=404, detail="Information System not found")
    
    # Create risk
    risk_data = threat_data.get('risk', {})
    risk = crud.create_risk(db, schemas.Risk(
        # Threat Agent Factors
        skill_level=risk_data.get('skill_level', 0),
        motive=risk_data.get('motive', 0),
        opportunity=risk_data.get('opportunity', 0),
        size=risk_data.get('size', 0),
        # Vulnerability Factors
        ease_of_discovery=risk_data.get('ease_of_discovery', 0),
        ease_of_exploit=risk_data.get('ease_of_exploit', 0),
        awareness=risk_data.get('awareness', 0),
        intrusion_detection=risk_data.get('intrusion_detection', 0),
        # Technical Impact
        loss_of_confidentiality=risk_data.get('loss_of_confidentiality', 0),
        loss_of_integrity=risk_data.get('loss_of_integrity', 0),
        loss_of_availability=risk_data.get('loss_of_availability', 0),
        loss_of_accountability=risk_data.get('loss_of_accountability', 0),
        # Business Impact
        financial_damage=risk_data.get('financial_damage', 0),
        reputation_damage=risk_data.get('reputation_damage', 0),
        non_compliance=risk_data.get('non_compliance', 0),
        privacy_violation=risk_data.get('privacy_violation', 0)
    ))
    
    # Create remediation
    remediation_data = threat_data.get('remediation', {})
    control_tags = remediation_data.get('control_tags', [])
    remediation = crud.create_remediation(
        db, 
        remediation_data.get('description', ''),
        control_tags
    )
    
    # Create threat
    # Normalize STRIDE category for manual threat
    raw_type = threat_data.get('type', 'Spoofing')
    normalized_type = normalize_stride_category(raw_type)
    if not normalized_type:
        normalized_type = 'Spoofing'
    
    threat = crud.create_threat(
        db,
        title=threat_data.get('title', 'New Threat'),
        description=threat_data.get('description', ''),
        type=normalized_type,
        information_system_id=system_uuid,
        risk_id=risk.id,
        remediation_id=remediation.id
    )
    
    # Eager load the created threat
    created_threat = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.id == threat.id).first()
    
    return created_threat

@app.get("/information_systems", response_model=list[schemas.InformationSystem])
async def read_information_systems(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    information_systems = crud.get_information_systems(db, skip=skip, limit=limit)
    return information_systems

@app.get("/information_systems/{information_system_id}", response_model=schemas.InformationSystem)
async def read_information_system(information_system_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_information_system = crud.get_information_system(db, information_system_id=information_system_id)
    if db_information_system is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_information_system

@app.post("/evaluate/{information_system_id}")
async def evaluate(file: UploadFile, information_system_id: str, db: Session = Depends(database.get_db)):
    try:
        # Save the image and get base64
        image_b64, saved_filename = save_image(file)
        
        if not image_b64 or not saved_filename:
            return {"message": "Error processing image", "success": False}
            
        db_information_system = crud.attach_diagram(db, information_system_id=information_system_id, image_path=saved_filename)
        
        # Get AI analysis
        result = clientAI(image_b64)
        
        # Verify that result is an object with 'threats' property
        if isinstance(result, str):
            # If it's a string, it's an error or message
            return {"information_system": db_information_system, "message": "Could not analyze diagram correctly", "success": False}
        
        # Verify it has threats property and is iterable
        if not hasattr(result, 'threats') or not result.threats:
            return {"information_system": db_information_system, "message": "No threats found in diagram", "success": False}
            
        # Process found threats
        for i in result.threats:
            # Normalize STRIDE category
            normalized_type = normalize_stride_category(i.type)
            if not normalized_type:
                normalized_type = 'Spoofing'  # Default fallback
            
            # Extract remediation data - can be string or object
            if hasattr(i.remediation, 'description'):
                # New structure with object
                remediation_desc = i.remediation.description
                control_tags = getattr(i.remediation, 'control_tags', [])
            else:
                # Old structure with string
                remediation_desc = str(i.remediation)
                control_tags = []
            
            remediation = crud.create_remediation(db, remediation_desc, control_tags)
            risk = crud.create_risk(db, i.risk)
            threat = crud.create_threat(db, i.title, i.description, normalized_type, UUID(information_system_id), risk.id, remediation.id)
        
        return {"information_system": db_information_system, "message": f"Diagram analyzed successfully and found {len(result.threats)} threats", "success": True}
    
    except Exception as e:
        return {"message": f"Error during processing: {str(e)}", "success": False}


@app.post("/new", response_model=schemas.InformationSystem)
async def evaluate(information_system:schemas.InformationSystemBaseCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_information_system = crud.create_information_system(db, information_system=information_system)
    return db_information_system

# Endpoint to update the risks of all threats associated with an information_system_id
@app.put("/information_systems/{information_system_id}/threats/risk/batch", response_model=list[schemas.Threat])
async def update_threats_risk_by_system(
    information_system_id: str,
    threats_data: list = Body(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Convert the id to UUID
    try:
        system_uuid = UUID(information_system_id)
    except Exception:
        raise HTTPException(status_code=400, detail="The system id is not a valid UUID")

    # Validate payload format
    if not isinstance(threats_data, list):
        raise HTTPException(status_code=400, detail="The payload must be a list of objects with threat_id and fields to update")
    for t in threats_data:
        if not isinstance(t, dict) or 'threat_id' not in t:
            raise HTTPException(status_code=400, detail="Each object must have the 'threat_id' key")

    # Filter threats using the UUID correctly
    threats = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.information_system_id == system_uuid).all()
    threats_by_id = {str(threat.id): threat for threat in threats}

    updated_threats = []
    for threat_update in threats_data:
        threat_id = str(threat_update.get('threat_id'))
        threat_data = threat_update.copy()
        threat_data.pop('threat_id', None)
        
        threat = threats_by_id.get(threat_id)
        if not threat:
            continue
        
        # Update basic threat information if provided
        if 'title' in threat_data:
            threat.title = threat_data['title']
        if 'type' in threat_data:
            # Normalize STRIDE category
            raw_type = threat_data['type']
            normalized_type = normalize_stride_category(raw_type)
            if normalized_type:
                threat.type = normalized_type
        if 'description' in threat_data:
            threat.description = threat_data['description']
        
        # Update risk
        risk_fields = ['skill_level', 'motive', 'opportunity', 'size', 'ease_of_discovery', 
                      'ease_of_exploit', 'awareness', 'intrusion_detection', 'loss_of_confidentiality',
                      'loss_of_integrity', 'loss_of_availability', 'loss_of_accountability',
                      'financial_damage', 'reputation_damage', 'non_compliance', 'privacy_violation',
                      'residual_risk']
        
        risk_data = {k: v for k, v in threat_data.items() if k in risk_fields}
        if risk_data:
            updated_risk = crud.update_threat_risk(db, threat_id, risk_data)
        
        # Update remediation if provided
        if 'remediation' in threat_data:
            remediation_data = threat_data['remediation']
            updated_remediation = crud.update_remediation(
                db, 
                threat.remediation_id,
                remediation_data.get('description', threat.remediation.description),
                remediation_data.get('status', threat.remediation.status),
                remediation_data.get('control_tags', threat.remediation.control_tags or [])
            )
        
        # Refresh the threat with updated data
        db.refresh(threat)
        updated_threats.append(threat)

    if not updated_threats:
        raise HTTPException(status_code=404, detail="No threats updated")
    return updated_threats

# Authentication endpoints
@app.post("/users", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username is already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


# Endpoints for security control tags
# =====================================================
# CONTROL TAGS HIERARCHY ENDPOINTS (specific routes first)
# =====================================================

@app.get("/control-tags/standards")
async def get_available_standards(
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get list of all available security standards
    """
    try:
        standards = crud.get_available_standards()
        return {
            "standards": standards,
            "total_standards": len(standards)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting standards: {str(e)}")


@app.get("/control-tags/hierarchy")
async def get_control_tags_hierarchy(
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get complete summary of control tags hierarchy
    """
    try:
        hierarchy = crud.get_control_tags_hierarchy_summary()
        return hierarchy
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting hierarchy: {str(e)}")


@app.get("/control-tags/by-standard/{standard}")
async def get_control_tags_by_standard(
    standard: str,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get all control tags from a specific standard
    """
    try:
        result = crud.get_control_tags_by_standard(standard)
        if result["total_controls"] == 0:
            raise HTTPException(
                status_code=404, 
                detail=f"Standard '{standard}' not found or has no controls"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting controls by standard: {str(e)}")


@app.get("/control-tags/by-standard/{standard}/category/{stride_category}")
async def get_control_tags_by_standard_and_stride(
    standard: str,
    stride_category: str,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get control tags from a specific standard filtered by STRIDE category
    """
    try:
        result = crud.get_control_tags_by_standard_and_stride(standard, stride_category)
        if result is None:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid STRIDE category '{stride_category}'"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting controls by standard and STRIDE: {str(e)}")


@app.post("/control-tags/categorize")
async def categorize_control_tags(
    tags: List[str] = Body(...),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Categorize a list of tags by standard
    """
    try:
        categorized = control_tags.categorize_tags(tags)
        return {
            "input_tags": tags,
            "categorized": categorized,
            "total_by_standard": {k: len(v) for k, v in categorized.items() if v}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error categorizing tags: {str(e)}")


@app.get("/control-tags/suggestions/{stride_category}")
async def get_control_tag_suggestions(
    stride_category: str,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get control tag suggestions based on STRIDE category with complete details
    """
    try:
        # Get unformatted suggestions
        raw_suggestions = control_tags.get_suggested_tags_for_stride(stride_category)
        
        # Format suggestions with standard in parentheses and get details
        formatted_suggestions = []
        detailed_suggestions = []
        
        for tag in raw_suggestions:
            formatted_tag = control_tags.format_tag_for_display(tag)
            formatted_suggestions.append(formatted_tag)
            
            # Get details for tooltip
            tag_details = control_tags.get_tag_details(tag)
            detailed_suggestions.append({
                "tag": tag,
                "formatted_tag": formatted_tag,
                "standard": tag_details["standard"],
                "category": tag_details["category"],
                "title": tag_details["title"],
                "description": tag_details["description"]
            })
        
        return {
            "stride_category": stride_category.upper(),
            "suggested_tags": formatted_suggestions,  # For backward compatibility
            "detailed_suggestions": detailed_suggestions,  # New response with details
            "categorized": control_tags.categorize_tags(raw_suggestions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting tag suggestions: {str(e)}")


@app.get("/control-tags/validate/{tag}")
async def validate_control_tag(
    tag: str,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Validate control tag format
    """
    try:
        is_valid = control_tags.validate_control_tag(tag)
        return {
            "tag": tag,
            "is_valid": is_valid,
            "message": "Valid control tag format" if is_valid else "Invalid control tag format"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating tag: {str(e)}")


# =====================================================
# END CONTROL TAGS ENDPOINTS  
# =====================================================


# Endpoint to update remediation with tags
@app.put("/remediations/{remediation_id}")
async def update_remediation(
    remediation_id: str,
    remediation_update: schemas.RemediationUpdate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(database.get_db)
):
    """
    Update a remediation including its control tags
    """
    try:
        remediation = crud.update_remediation(
            db,
            remediation_id,
            remediation_update.description,
            remediation_update.status,
            remediation_update.control_tags
        )
        
        if not remediation:
            raise HTTPException(status_code=404, detail="Remediation not found")
        
        return schemas.Remediation.from_orm(remediation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating remediation: {str(e)}")


# Specific endpoint to update control tags of a threat
@app.put("/threats/{threat_id}/remediation/tags")
async def update_threat_remediation_tags(
    threat_id: str,
    tags_update: dict,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(database.get_db)
):
    """
    Update only the control tags of a threat's remediation
    """
    try:
        # Get the threat
        threat = db.query(models.Threat).filter(models.Threat.id == threat_id).first()
        if not threat:
            raise HTTPException(status_code=404, detail="Threat not found")
        
        # Get associated remediation
        if not threat.remediation_id:
            raise HTTPException(status_code=404, detail="Threat has no associated remediation")
        
        remediation = db.query(models.Remediation).filter(
            models.Remediation.id == threat.remediation_id
        ).first()
        
        if not remediation:
            raise HTTPException(status_code=404, detail="Remediation not found")
        
        # Update control tags
        control_tags = tags_update.get('control_tags', [])
        remediation.control_tags = json.dumps(control_tags) if control_tags else None
        
        db.commit()
        db.refresh(remediation)
        
        return {
            "threat_id": threat_id,
            "remediation_id": remediation.id,
            "control_tags": control_tags,
            "message": "Control tags updated successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating control tags: {str(e)}")


# Endpoints for advanced remediation filtering
@app.get("/api/remediations/filter")
async def filter_remediations(
    control_standard: Optional[str] = None,  # ASVS, MASVS, SBS, ISO27001, NIST
    control_tag: Optional[str] = None,       # Specific tag like "ASVS-V2.1.1"
    stride_category: Optional[str] = None,   # S, T, R, I, D, E
    status: Optional[bool] = None,           # True/False for completed status
    information_system_id: Optional[str] = None,  # Filter by system
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Filter remediations by multiple criteria:
    - Control standard (ASVS, MASVS, etc.)
    - Specific control tag
    - STRIDE category of associated threat
    - Remediation status
    - Information system
    """
    try:
        # Build base query with necessary joins
        query = db.query(models.Remediation).join(
            models.Threat, models.Threat.remediation_id == models.Remediation.id
        )
        
        # Filter by information system
        if information_system_id:
            query = query.filter(models.Threat.information_system_id == information_system_id)
        
        # Filter by STRIDE category
        if stride_category:
            normalized_stride = normalize_stride_category(stride_category)
            query = query.filter(models.Threat.type == normalized_stride)
        
        # Filter by remediation status
        if status is not None:
            query = query.filter(models.Remediation.status == status)
        
        # Filter by control tags
        if control_standard:
            query = query.filter(models.Remediation.control_tags.like(f'%{control_standard}-%'))
        
        if control_tag:
            query = query.filter(models.Remediation.control_tags.like(f'%{control_tag}%'))
        
        remediations = query.distinct().all()
        
        # Convert results with additional information
        result = []
        for remediation in remediations:
            # Get associated threats
            threats = db.query(models.Threat).filter(
                models.Threat.remediation_id == remediation.id
            ).all()
            
            remediation_data = schemas.Remediation.from_orm(remediation).dict()
            remediation_data['associated_threats'] = [
                {
                    'id': str(threat.id),
                    'title': threat.title,
                    'type': threat.type,  # STRIDE category
                    'information_system_id': str(threat.information_system_id)
                }
                for threat in threats
            ]
            result.append(remediation_data)
        
        return {
            "remediations": result,
            "total": len(result),
            "filters_applied": {
                "control_standard": control_standard,
                "control_tag": control_tag,
                "stride_category": stride_category,
                "status": status,
                "information_system_id": information_system_id
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering remediations: {str(e)}")


@app.get("/api/remediations/by-control-standard/{standard}")
async def get_remediations_by_control_standard(
    standard: str,  # ASVS, MASVS, SBS, ISO27001, NIST
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all remediations that have tags from a specific standard
    """
    try:
        remediations = db.query(models.Remediation).filter(
            models.Remediation.control_tags.like(f'%{standard}-%')
        ).all()
        
        result = []
        for remediation in remediations:
            remediation_data = schemas.Remediation.from_orm(remediation).dict()
            
            # Filter tags from requested standard
            if remediation.control_tags:
                import json
                all_tags = json.loads(remediation.control_tags)
                filtered_tags = [tag for tag in all_tags if tag.startswith(f"{standard}-")]
                remediation_data['filtered_control_tags'] = filtered_tags
            
            # Get associated threats
            threats = db.query(models.Threat).filter(
                models.Threat.remediation_id == remediation.id
            ).all()
            
            remediation_data['threat_count'] = len(threats)
            remediation_data['stride_categories'] = list(set([threat.type for threat in threats]))
            
            result.append(remediation_data)
        
        return {
            "standard": standard,
            "remediations": result,
            "total": len(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting remediations by standard: {str(e)}")


@app.get("/api/remediations/by-stride/{stride_category}")
async def get_remediations_by_stride(
    stride_category: str,  # S, T, R, I, D, E
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all remediations associated with threats from a specific STRIDE category
    """
    try:
        normalized_stride = normalize_stride_category(stride_category)
        
        # Search for threats from STRIDE category
        threats = db.query(models.Threat).filter(
            models.Threat.type == normalized_stride
        ).all()
        
        # Get unique remediations
        remediation_ids = list(set([threat.remediation_id for threat in threats]))
        remediations = db.query(models.Remediation).filter(
            models.Remediation.id.in_(remediation_ids)
        ).all()
        
        result = []
        for remediation in remediations:
            remediation_data = schemas.Remediation.from_orm(remediation).dict()
            
            # Get threats from this category associated with the remediation
            associated_threats = [t for t in threats if t.remediation_id == remediation.id]
            remediation_data['stride_threats'] = [
                {
                    'id': str(threat.id),
                    'title': threat.title,
                    'description': threat.description,
                    'information_system_id': str(threat.information_system_id)
                }
                for threat in associated_threats
            ]
            
            # Suggest relevant tags for this STRIDE category
            suggested_tags = control_tags.get_suggested_tags_for_stride(stride_category)
            remediation_data['suggested_control_tags'] = suggested_tags
            
            result.append(remediation_data)
        
        return {
            "stride_category": normalized_stride,
            "remediations": result,
            "total": len(result),
            "suggested_tags": control_tags.get_suggested_tags_for_stride(stride_category)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting remediations by STRIDE: {str(e)}")


@app.get("/api/remediations/statistics")
async def get_remediation_statistics(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get remediation statistics by control standards and STRIDE categories
    """
    try:
        stats = crud.get_remediation_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")


@app.get("/control-tags/existing")
async def get_existing_control_tags(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all control tags that already exist in the system
    """
    try:
        existing_tags = crud.get_all_existing_control_tags(db)
        return {
            "existing_tags": existing_tags,
            "categorized": control_tags.categorize_tags(existing_tags),
            "total": len(existing_tags)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting existing tags: {str(e)}")


@app.get("/control-tags/search")
async def search_control_tags(
    query: str,
    include_existing: bool = True,
    include_predefined: bool = True,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search control tags (existing + predefined)
    """
    try:
        results = []
        
        # Search in predefined tags
        if include_predefined:
            predefined_tags = control_tags.search_predefined_tags(query)
            results.extend(predefined_tags)
        
        # Enrich results with details
        detailed_results = []
        formatted_results = []
        for tag in results[:20]:  # Limit to 20 results
            tag_details = control_tags.get_tag_details(tag)
            formatted_tag = control_tags.format_tag_for_display(tag)
            
            detailed_results.append({
                "tag": formatted_tag,  # Tag with parentheses
                "standard": tag_details["standard"],
                "category": tag_details["category"],
                "title": tag_details["title"],
                "description": tag_details["description"]
            })
            formatted_results.append(formatted_tag)
        
        return {
            "query": query,
            "results": formatted_results,  # Tags with parentheses
            "detailed_results": detailed_results,  # With formatted tags
            "categorized": control_tags.categorize_tags(formatted_results),
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching tags: {str(e)}")
