from typing import Optional
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, FilePath
from datetime import datetime

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

class Remediation(BaseModel):
    model_config = {"from_attributes": True}
    
    description: str
    status: bool = False


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


# Para actualización parcial de usuario (por ejemplo, solo password)
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
