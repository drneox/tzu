import datetime
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID, DateTime, Text, Float
from sqlalchemy.orm import relationship


from database import Base


class Risk(Base):
    __tablename__ = "risks"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    
    # OWASP Risk Rating - Likelihood Factors
    # Threat Agent Factors
    skill_level = Column(Integer)  # 0-9 scale
    motive = Column(Integer)       # 0-9 scale  
    opportunity = Column(Integer)  # 0-9 scale
    size = Column(Integer)         # 0-9 scale
    
    # Vulnerability Factors
    ease_of_discovery = Column(Integer)    # 0-9 scale
    ease_of_exploit = Column(Integer)      # 0-9 scale
    awareness = Column(Integer)            # 0-9 scale
    intrusion_detection = Column(Integer)  # 0-9 scale
    
    # OWASP Risk Rating - Impact Factors
    # Technical Impact
    loss_of_confidentiality = Column(Integer)  # 0-9 scale
    loss_of_integrity = Column(Integer)        # 0-9 scale
    loss_of_availability = Column(Integer)     # 0-9 scale
    loss_of_accountability = Column(Integer)   # 0-9 scale
    
    # Business Impact
    financial_damage = Column(Integer)      # 0-9 scale
    reputation_damage = Column(Integer)     # 0-9 scale
    non_compliance = Column(Integer)        # 0-9 scale
    privacy_violation = Column(Integer)     # 0-9 scale
    
    # Residual Risk (calculated or manually set)
    residual_risk = Column(Float)  # 1-9 scale (allows decimal values)


class Remediation(Base):
    __tablename__ = "remediations"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    description = Column(Text)
    status = Column(Boolean, default=False)
    

class Threat(Base):
    __tablename__ = "threats"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String)
    type = Column(String)
    description = Column(Text)
    information_system_id = Column(UUID,ForeignKey("information_systems.id")) 
    remediation_id = Column(UUID,ForeignKey("remediations.id"))  
    risk_id = Column(UUID,ForeignKey("risks.id"))  
    information_system = relationship("InformationSystem", back_populates="threats")
    remediation = relationship("Remediation")
    risk = relationship("Risk")
    
    
class InformationSystem(Base):
    __tablename__ = "information_systems"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    diagram = Column(Text)
    threats = relationship("Threat", back_populates="information_system", cascade="all, delete-orphan")


class UseCase(Base):
    __tablename__ = "use_cases"
    id = Column(UUID, primary_key=True)
    title = Column(String)
    description = Column(Text)
    information_system_id = Column(UUID,ForeignKey("information_systems.id"))  

    information_system = relationship("InformationSystem")


class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password_hash = Column(String(128))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

