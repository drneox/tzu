import datetime
import uuid
import json

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

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
    
    @hybrid_property
    def likelihood_score(self):
        """Calculate OWASP likelihood score (average of threat agent + vulnerability factors)"""
        if any(factor is None for factor in [
            self.skill_level, self.motive, self.opportunity, self.size,
            self.ease_of_discovery, self.ease_of_exploit, self.awareness, self.intrusion_detection
        ]):
            return 0
        
        threat_agent = (self.skill_level + self.motive + self.opportunity + self.size) / 4
        vulnerability = (self.ease_of_discovery + self.ease_of_exploit + self.awareness + self.intrusion_detection) / 4
        return (threat_agent + vulnerability) / 2
    
    @hybrid_property
    def impact_score(self):
        """Calculate OWASP impact score (average of technical + business impact factors)"""
        if any(factor is None for factor in [
            self.loss_of_confidentiality, self.loss_of_integrity, self.loss_of_availability, self.loss_of_accountability,
            self.financial_damage, self.reputation_damage, self.non_compliance, self.privacy_violation
        ]):
            return 0
        
        technical_impact = (self.loss_of_confidentiality + self.loss_of_integrity + 
                           self.loss_of_availability + self.loss_of_accountability) / 4
        business_impact = (self.financial_damage + self.reputation_damage + 
                          self.non_compliance + self.privacy_violation) / 4
        return (technical_impact + business_impact) / 2
    
    @hybrid_property
    def overall_risk_score(self):
        """Calculate overall OWASP risk score"""
        return (self.likelihood_score + self.impact_score) / 2
    
    @hybrid_property
    def inherit_risk(self):
        """Calculate inherent risk level based on OWASP methodology"""
        score = self.overall_risk_score
        
        if score < 3:
            return "LOW"
        elif score < 6:
            return "MEDIUM" 
        elif score < 9:
            return "HIGH"
        else:
            return "CRITICAL"
    
    @inherit_risk.expression
    def inherit_risk(cls):
        """SQL expression for risk level calculation"""
        from sqlalchemy import case, and_
        
        # Calculate likelihood score (average of threat agent + vulnerability factors)
        threat_agent = (cls.skill_level + cls.motive + cls.opportunity + cls.size) / 4.0
        vulnerability = (cls.ease_of_discovery + cls.ease_of_exploit + cls.awareness + cls.intrusion_detection) / 4.0
        likelihood = (threat_agent + vulnerability) / 2.0
        
        # Calculate impact score (average of technical + business impact factors)  
        technical_impact = (cls.loss_of_confidentiality + cls.loss_of_integrity + 
                           cls.loss_of_availability + cls.loss_of_accountability) / 4.0
        business_impact = (cls.financial_damage + cls.reputation_damage + 
                          cls.non_compliance + cls.privacy_violation) / 4.0
        impact = (technical_impact + business_impact) / 2.0
        
        # Calculate overall score
        overall_score = (likelihood + impact) / 2.0
        
        return case(
            (overall_score < 3, "LOW"),
            (overall_score < 6, "MEDIUM"),
            (overall_score < 9, "HIGH"),
            else_="CRITICAL"
        )
    
    def current_risk(self, remediation_status=False):
        """
        Calculate current risk level considering remediation status.
        If remediation is applied (status=True), returns residual_risk level.
        Otherwise, returns inherit_risk level.
        """
        if remediation_status and self.residual_risk is not None:
            # Convert residual_risk (float) to risk level
            if self.residual_risk < 3:
                return "LOW"
            elif self.residual_risk < 6:
                return "MEDIUM"
            elif self.residual_risk < 9:
                return "HIGH"
            else:
                return "CRITICAL"
        else:
            # Return inherent risk if no remediation applied
            return self.inherit_risk


class Remediation(Base):
    __tablename__ = "remediations"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    description = Column(Text)
    status = Column(Boolean, default=False)
    # Tags flexibles para controles de seguridad (JSON array de strings)
    # Ejemplos: ["ASVS-V2.1.1", "MASVS-MSTG-AUTH-1", "SBS-Circular-G-140-2009", "ISO27001-A.9.1.1"]
    control_tags = Column(Text)  # JSON string array
    
    @hybrid_property
    def control_tags_list(self):
        """Convierte control_tags JSON string a lista de Python"""
        if not self.control_tags or self.control_tags == "[]":
            return []
        try:
            return json.loads(self.control_tags)
        except (json.JSONDecodeError, TypeError):
            return []
    
    @control_tags_list.setter
    def control_tags_list(self, value):
        """Convierte lista de Python a JSON string para almacenamiento"""
        if value is None:
            self.control_tags = None
        else:
            self.control_tags = json.dumps(value)
    

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
    
    @property
    def current_risk_level(self):
        """
        Calculate current risk level considering remediation status.
        If remediation is applied (status=True), considers residual_risk.
        Otherwise, returns inherit_risk.
        """
        if self.risk and self.remediation:
            return self.risk.current_risk(self.remediation.status)
        elif self.risk:
            return self.risk.inherit_risk
        else:
            return "UNKNOWN"
    
    
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

