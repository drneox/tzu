from typing import Optional
from typing import List, Optional, Literal
from uuid import UUID
from pydantic import BaseModel, FilePath, field_validator, Field
from datetime import datetime
import json

class InformationSystemCreate(BaseModel):
    title: str
    description: str | None = None
    project_id: Optional[UUID] = None
    project_name: Optional[str] = None

class InformationSystemBase(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    project_id: Optional[UUID] = None
    project_name: Optional[str] = None
    archived: bool = False
  

class InformationSystemBaseCreate(InformationSystemCreate):
    pass


class UseCase(BaseModel):
    model_config = {"from_attributes": True}
    
    id: UUID
    title: str
    description:str
    information_system_id: str

class RemediationBase(BaseModel):
    description: str
    status: bool = False
    control_tags: Optional[List[str]] = []  # Lista de tags de controles

class RemediationCreate(RemediationBase):
    pass

class RemediationUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[bool] = None
    control_tags: Optional[List[str]] = None

class Remediation(RemediationBase):
    model_config = {"from_attributes": True}
    
    id: UUID
    
    @field_validator('control_tags', mode='before')
    @classmethod
    def parse_control_tags(cls, v):
        """Parse control_tags from JSON string or return as-is if already a list.
        Also validates and corrects tags (fixes orphans from old LLM output)."""
        if v is None:
            return []
        elif isinstance(v, str):
            if v == "" or v == "[]":
                return []
            try:
                parsed = json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        elif isinstance(v, list):
            parsed = v
        else:
            return []

        # Normalize tags: fix orphans, correct SBS subnumerals, accept valid formats
        try:
            from standards import validate_and_correct_control_tags
            return validate_and_correct_control_tags(parsed)
        except Exception:
            return parsed


class Risk(BaseModel):
    model_config = {"from_attributes": True}
    
    # OWASP Risk Rating - Likelihood Factors
    # Threat Agent Factors
    skill_level: int = 0          # 0-9 scale
    motive: int = 0              # 0-9 scale  
    opportunity: int = 0         # 0-9 scale
    size: int = 0                # 0-9 scale
    
    # Vulnerability Factors
    ease_of_discovery: int = 0   # 0-9 scale
    ease_of_exploit: int = 0     # 0-9 scale
    awareness: int = 0           # 0-9 scale
    intrusion_detection: int = 0 # 0-9 scale
    
    # OWASP Risk Rating - Impact Factors
    # Technical Impact
    loss_of_confidentiality: int = 0  # 0-9 scale
    loss_of_integrity: int = 0        # 0-9 scale
    loss_of_availability: int = 0     # 0-9 scale
    loss_of_accountability: int = 0   # 0-9 scale
    
    # Business Impact
    financial_damage: int = 0         # 0-9 scale
    reputation_damage: int = 0        # 0-9 scale
    non_compliance: int = 0           # 0-9 scale
    privacy_violation: int = 0        # 0-9 scale
    
    # Residual Risk (calculated or manually set)
    residual_risk: Optional[float] = None  # 1-9 scale (allows decimal values)
    
    # Calculated properties (read-only)
    likelihood_score: Optional[float] = None
    impact_score: Optional[float] = None
    overall_risk_score: Optional[float] = None
    inherit_risk: Optional[str] = None


class Threat(BaseModel):
    model_config = {"from_attributes": True}
    
    id: UUID
    type: str
    title:str
    description:str
    remediation: Remediation
    risk: Risk
    current_risk_level: Optional[str] = None

class InformationSystem(InformationSystemBase):
    model_config = {"from_attributes": True}

    id: UUID
    datetime: datetime
    diagram: str | None = None
    diagram_input_type: str | None = None  # "image" | "text"
    archived: bool = False
    threats: List[Threat] = []

class ThreatWithSystem(BaseModel):
    model_config = {"from_attributes": True}
    
    id: UUID
    type: str
    title: str
    description: str
    remediation: Remediation
    risk: Risk
    information_system: InformationSystem  # Usar la clase ya definida arriba
    current_risk_level: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: str
    name: str


class UserCreate(UserBase):
    password: str
    role: Literal["admin", "analyst", "reader"] = "reader"


# For partial user update (for example, password only)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    model_config = {"from_attributes": True}
    
    id: UUID
    created_at: datetime
    is_active: bool = True
    is_admin: bool = False
    role: str = "reader"


class UserRoleUpdate(BaseModel):
    role: Literal["admin", "analyst", "reader"]


class UserActiveUpdate(BaseModel):
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserLogin(BaseModel):
    username: str


class AuditLogEntry(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    action: str
    target_user_id: Optional[UUID] = None
    performed_by_id: UUID
    timestamp: datetime
    detail: Optional[str] = None


# =====================================================
# PROJECT SCHEMAS
# =====================================================

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    model_config = {"from_attributes": True}

    id: UUID
    created_at: datetime
    created_by: UUID


class ProjectWithCounts(ProjectResponse):
    analysis_count: int = 0
    member_count: int = 0


class ProjectMemberAdd(BaseModel):
    user_id: UUID


class ProjectMemberBase(BaseModel):
    model_config = {"from_attributes": True}

    user_id: UUID
    username: str
    name: str
    role: str
    added_at: datetime
    added_by: Optional[UUID] = None


# =====================================================
# INFORMATION SYSTEM UPDATE SCHEMA
# =====================================================

class InformationSystemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[UUID] = None
    project_name_inline: Optional[str] = None  # Creates a new project inline if provided


# =====================================================
# DASHBOARD SCHEMAS
# =====================================================

class ThreatsByLevel(BaseModel):
    CRITICAL: int = 0
    HIGH: int = 0
    MEDIUM: int = 0
    LOW: int = 0
    UNKNOWN: int = 0


class SystemExposure(BaseModel):
    id: str
    title: str
    project_name: Optional[str] = None
    critical_count: int
    high_count: int
    total_threats: int


class ProjectExposure(BaseModel):
    id: Optional[str] = None
    name: str
    critical_count: int
    high_count: int
    total_threats: int
    system_count: int


class StandardsCoverage(BaseModel):
    NIST: float = 0.0
    ISO27001: float = 0.0
    ASVS: float = 0.0
    MASVS: float = 0.0
    SBS: float = 0.0


class StandardsRemediation(BaseModel):
    NIST: float = 0.0
    ISO27001: float = 0.0
    ASVS: float = 0.0
    MASVS: float = 0.0
    SBS: float = 0.0


class DashboardStats(BaseModel):
    total_systems: int
    total_threats: int
    threats_by_level: ThreatsByLevel
    remediation_rate: float
    top_systems: List[SystemExposure]
    top_projects: List[ProjectExposure] = []
    standards_coverage: StandardsCoverage
    standards_remediation: StandardsRemediation
    filtered_by_project: Optional[str] = None
