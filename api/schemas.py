from typing import Optional
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, FilePath, field_validator, Field
from datetime import datetime
import json

class InformationSystemBase(BaseModel):
    title: str
    description: str | None = None
  

class InformationSystemBaseCreate(InformationSystemBase):
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
        """Parse control_tags from JSON string or return as-is if already a list"""
        if v is None:
            return []
        elif isinstance(v, str):
            if v == "" or v == "[]":
                return []
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        elif isinstance(v, list):
            return v
        else:
            return []


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


class Threat(BaseModel):
    model_config = {"from_attributes": True}
    
    id: UUID
    type: str
    title:str
    description:str
    remediation: Remediation
    risk: Risk

class ThreatWithSystem(BaseModel):
    model_config = {"from_attributes": True}
    
    id: UUID
    type: str
    title: str
    description: str
    remediation: Remediation
    risk: Risk
    information_system: InformationSystemBase
  
class InformationSystem(InformationSystemBase):
    model_config = {"from_attributes": True}
    
    id: UUID
    datetime: datetime
    diagram: str | None = None
    threats: List[Threat] = []


class UserBase(BaseModel):
    username: str
    email: str
    name: str


class UserCreate(UserBase):
    password: str


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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str
