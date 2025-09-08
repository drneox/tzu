from uuid import UUID
import json
import models
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, text
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional, Dict, Union, List

import schemas

# Import STRIDE normalization function
from stride_validator import normalize_stride_category

def get_all_threats(db: Session, skip: int = 0, limit: int = 100, system_id: Optional[str] = None, standards: Optional[list] = None, inherit_risk: Optional[str] = None, current_risk: Optional[str] = None):
    """Gets all threats with optional filters"""
    
    query = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation),
        joinedload(models.Threat.information_system)
    )
    
    # Filter by information system
    if system_id:
        try:
            query = query.filter(models.Threat.information_system_id == UUID(system_id))
        except ValueError:
            return []
    
        # Filtro por riesgo inherente
    if inherit_risk:
        query = query.join(models.Risk).filter(models.Risk.inherit_risk == inherit_risk)
    
    # Filtro por riesgo actual (considerando estado de remediación)
    if current_risk:
        from sqlalchemy import case, and_
        
        # Unir con Risk y Remediation si no se han unido ya
        if not inherit_risk:
            query = query.join(models.Risk)
        query = query.join(models.Remediation)
        
        # Crear lógica condicional para riesgo actual:
        # Si remediation.status = True Y residual_risk no es NULL, usar residual_risk
        # Sino, usar inherit_risk
        current_risk_expression = case(
            (
                and_(
                    models.Remediation.status == True,
                    models.Risk.residual_risk.isnot(None)
                ),
                case(
                    (models.Risk.residual_risk < 3, "LOW"),
                    (models.Risk.residual_risk < 6, "MEDIUM"),
                    (models.Risk.residual_risk < 9, "HIGH"),
                    else_="CRITICAL"
                )
            ),
            else_=models.Risk.inherit_risk
        )
        
        query = query.filter(current_risk_expression == current_risk)
    
    # Filtro por estándares - usando SQL directo para JSON
    if standards and len(standards) > 0:
        # Usar la lógica SQL que funciona correctamente
        for standard in standards:
            condition = text("""
                EXISTS (
                    SELECT 1 FROM remediations r 
                    CROSS JOIN LATERAL json_array_elements_text(r.control_tags::json) AS tag
                    WHERE r.id = threats.remediation_id 
                    AND tag LIKE :pattern
                )
            """).params(pattern=f'%({standard})')
            
            query = query.filter(condition)
    
    # Get threats ordered by ID (newest first, assuming UUIDs are generated chronologically)
    threats = query.order_by(models.Threat.id.desc()).offset(skip).limit(limit).all()
    
    return threats


# Security configuration for passwords and JWT
import os
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, is_admin: bool = False):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        name=user.name,
        password_hash=hashed_password,
        is_active=True,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    print(f"[DEBUG] Searching user: {repr(username)} -> Found: {user is not None}")
    if user:
        print(f"[DEBUG] Hash in DB: {repr(user.password_hash)}")
    if not user:
        return False
    try:
        valido = verify_password(password, user.password_hash)
        print(f"[DEBUG] Resultado verificación hash: {valido}")
    except Exception as e:
        print(f"[DEBUG] Error al verificar hash: {e}")
        return False
    if not valido:
        return False
    return user

def create_access_token(data: Dict[str, Union[str, datetime]], expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    # Add security claims
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Standard JWT claims for better security
    to_encode.update({
        "exp": expire,      # Expiration time
        "iat": now,         # Issued at time
        "nbf": now,         # Not before time
        "iss": "tzu-api",   # Issuer
        "aud": "tzu-client" # Audience
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def update_threat_risk(db: Session, threat_id: str, data: dict):
    threat = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.id == UUID(threat_id)).first()
    if not threat:
        return None
    risk = db.query(models.Risk).filter(models.Risk.id == threat.risk_id).first()
    remediation = db.query(models.Remediation).filter(models.Remediation.id == threat.remediation_id).first()
    
    # Update Threat fields
    for key in ['title', 'type', 'description']:
        if key in data:
            value = data[key]
            # Normalizar categoría STRIDE si es el campo 'type'
            if key == 'type':
                normalized_value = normalize_stride_category(value)
                if not normalized_value:
                    print(f"⚠️ Warning: Invalid STRIDE category '{value}' in update, using 'Spoofing'")
                    value = 'Spoofing'
                else:
                    value = normalized_value
            print(f"Actualizando Threat {key}: {getattr(threat, key)} -> {value}")
            setattr(threat, key, value)
    # Update Remediation field
    if remediation and 'remediation' in data and isinstance(data['remediation'], dict):
        remediation_data = data['remediation']
        print(f"Remediation data received: {remediation_data}")
        if 'description' in remediation_data:
            print(f"Updating Remediation description: {remediation.description} -> {remediation_data['description']}")
            remediation.description = remediation_data['description']
        if 'status' in remediation_data:
            print(f"Updating Remediation status: {remediation.status} -> {remediation_data['status']}")
            remediation.status = remediation_data['status']
        db.add(remediation)
        db.commit()
        db.refresh(remediation)
        print(f"Remediation actualizada: description={remediation.description}, status={remediation.status}")
    # Update Risk fields (OWASP Risk Rating)
    owasp_fields = [
        # Threat Agent Factors
        'skill_level', 'motive', 'opportunity', 'size',
        # Vulnerability Factors  
        'ease_of_discovery', 'ease_of_exploit', 'awareness', 'intrusion_detection',
        # Technical Impact
        'loss_of_confidentiality', 'loss_of_integrity', 'loss_of_availability', 'loss_of_accountability',
        # Business Impact
        'financial_damage', 'reputation_damage', 'non_compliance', 'privacy_violation',
        # Residual Risk
        'residual_risk'
    ]
    for key in owasp_fields:
        if key in data and risk:
            if key == 'residual_risk':
                print(f"Guardando riesgo residual: {data[key]}")
            setattr(risk, key, data[key])
    
    db.add(threat)
    if risk:
        db.add(risk)
    db.commit()
    db.refresh(threat)
    if risk:
        db.refresh(risk)
    if risk:
        db.refresh(risk)
    if remediation:
        db.refresh(remediation)
    return threat

def get_information_systems(db: Session,skip: int = 0, limit: int = 100):
    return db.query(models.InformationSystem).order_by(models.InformationSystem.datetime.desc()).offset(skip).limit(limit).all()
 
def get_information_system(db: Session, information_system_id: str):
    return db.query(models.InformationSystem).options(
        joinedload(models.InformationSystem.threats).joinedload(models.Threat.risk),
        joinedload(models.InformationSystem.threats).joinedload(models.Threat.remediation)
    ).filter(models.InformationSystem.id == UUID(information_system_id)).first()
 
def get_threats_by_information_system(db: Session, information_system_id: str):
    return db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.information_system_id == UUID(information_system_id)).order_by(models.Threat.created_at.desc()).all()
 
def create_information_system(db: Session, information_system: schemas.InformationSystem):
    db_information_system = models.InformationSystem(title=information_system.title,
                                                    description=information_system.description
                                                    )
    
    db.add(db_information_system)
    db.commit()
    db.refresh(db_information_system)
    return db_information_system

    
def create_use_case(db: Session, use_case: schemas.UseCase):
    db_use_case = models.InformationSystem(title=use_case.title,
                                                    description=use_case.description,
                                                    information_system_id=use_case.information_system_id
                                                    )
    db.add(db_use_case)
    db.commit()
    db.refresh()
    return db_use_case


def attach_diagram(db: Session, information_system_id: str, image_path: str):
    information_system = db.query(models.InformationSystem).filter(models.InformationSystem.id==UUID(information_system_id)).first()
    information_system.diagram = image_path
    db.add(information_system)
    db.commit()
    db.refresh(information_system)
    return information_system

def create_threat(db: Session, title:str, description:str, type:str, information_system_id: str, risk_id:str, remediation_id:str):
    threat = models.Threat(
        information_system_id=information_system_id,
        remediation_id= remediation_id,
        risk_id=risk_id,
        description=description,
        title=title,
        type=type,
        )
    db.add(threat)
    db.commit()
    db.refresh(threat)
    return threat

def create_risk(db: Session, risk: schemas.Risk):
    risk_model = models.Risk(
        # Threat Agent Factors
        skill_level = risk.skill_level,
        motive = risk.motive,
        opportunity = risk.opportunity,
        size = risk.size,
        # Vulnerability Factors
        ease_of_discovery = risk.ease_of_discovery,
        ease_of_exploit = risk.ease_of_exploit,
        awareness = risk.awareness,
        intrusion_detection = risk.intrusion_detection,
        # Technical Impact
        loss_of_confidentiality = risk.loss_of_confidentiality,
        loss_of_integrity = risk.loss_of_integrity,
        loss_of_availability = risk.loss_of_availability,
        loss_of_accountability = risk.loss_of_accountability,
        # Business Impact
        financial_damage = risk.financial_damage,
        reputation_damage = risk.reputation_damage,
        non_compliance = risk.non_compliance,
        privacy_violation = risk.privacy_violation,
        )
    db.add(risk_model)
    db.commit()
    db.refresh(risk_model)
    return risk_model


def create_remediation(db: Session, description: str, control_tags: list = None):
    # Convertir lista de control_tags a JSON string
    control_tags_json = json.dumps(control_tags) if control_tags else "[]"
    
    remediation = models.Remediation(
        description=description,
        status=False,
        control_tags=control_tags_json
    )
    db.add(remediation)
    db.commit()
    db.refresh(remediation)
    return remediation


def update_remediation(db: Session, remediation_id: str, description: str = None, status: bool = None, control_tags: list = None):
    """
    Update an existing remediation
    """
    try:
        # Search for remediation by ID
        remediation = db.query(models.Remediation).filter(models.Remediation.id == remediation_id).first()
        
        if not remediation:
            return None
        
        # Update fields if provided
        if description is not None:
            remediation.description = description
        
        if status is not None:
            remediation.status = status
        
        if control_tags is not None:
            # Convert control_tags list to JSON string
            control_tags_json = json.dumps(control_tags) if control_tags else "[]"
            remediation.control_tags = control_tags_json
        
        db.commit()
        db.refresh(remediation)
        return remediation
        
    except Exception as e:
        db.rollback()
        raise e


# Authentication utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# CRUD operations for users
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user




def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: UUID, user_data: schemas.UserBase):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    # Allow partial update and hash password if provided
    data = user_data.dict(exclude_unset=True)
    if "password" in data and data["password"]:
        db_user.password_hash = get_password_hash(data["password"])
        data.pop("password")
    for key, value in data.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user


def delete_threat(db: Session, threat_id: str):
    """
    Delete a threat and its associated risk and remediation.
    
    Args:
        db: Database session
        threat_id: UUID string of the threat to delete
        
    Returns:
        bool: True if threat was deleted, False if not found
    """
    from uuid import UUID
    
    # Convert string UUID to UUID object
    try:
        uuid_obj = UUID(threat_id)
    except ValueError:
        return False
    
    # Get the threat with relationships
    threat = db.query(models.Threat).filter(models.Threat.id == uuid_obj).first()
    if not threat:
        return False
    
    # Store IDs for cleanup
    risk_id = threat.risk_id
    remediation_id = threat.remediation_id
    
    # Delete the threat first
    db.delete(threat)
    
    # Delete associated risk
    if risk_id:
        risk = db.query(models.Risk).filter(models.Risk.id == risk_id).first()
        if risk:
            db.delete(risk)
    
    # Delete associated remediation
    if remediation_id:
        remediation = db.query(models.Remediation).filter(models.Remediation.id == remediation_id).first()
        if remediation:
            db.delete(remediation)
    
    # Commit all changes
    db.commit()
    return True

