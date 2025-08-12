import datetime
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID, DateTime, Text
from sqlalchemy.orm import relationship


from .database import Base


class Risk(Base):
    __tablename__ = "risks"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    damage = Column(Integer)
    reproducibility = Column(Integer)
    exploitability = Column(Integer)
    affected_users = Column(Integer)
    discoverability = Column(Integer)
    compliance = Column(Integer)


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

