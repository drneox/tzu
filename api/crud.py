from uuid import UUID
import models
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional, Dict, Union

import schemas

# Security configuration for passwords and JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Should be in a config file
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    print(f"[DEBUG] Buscando usuario: {repr(username)} -> Encontrado: {user is not None}")
    if user:
        print(f"[DEBUG] Hash en BD: {repr(user.password_hash)}")
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
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
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
            print(f"Actualizando Threat {key}: {getattr(threat, key)} -> {data[key]}")
            setattr(threat, key, data[key])
    # Update Remediation field
    if remediation and 'remediation' in data and isinstance(data['remediation'], dict):
        remediation_data = data['remediation']
        print(f"Datos de remediación recibidos: {remediation_data}")
        if 'description' in remediation_data:
            print(f"Actualizando Remediation description: {remediation.description} -> {remediation_data['description']}")
            remediation.description = remediation_data['description']
        if 'status' in remediation_data:
            print(f"Actualizando Remediation status: {remediation.status} -> {remediation_data['status']}")
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
    return db.query(models.InformationSystem).offset(skip).limit(limit).all()
 
def get_information_system(db: Session, information_system_id: str):
    return db.query(models.InformationSystem).options(
        joinedload(models.InformationSystem.threats).joinedload(models.Threat.risk),
        joinedload(models.InformationSystem.threats).joinedload(models.Threat.remediation)
    ).filter(models.InformationSystem.id == UUID(information_system_id)).first()
 
def get_threats_by_information_system(db: Session, information_system_id: str):
    return db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.information_system_id == UUID(information_system_id)).all()
 
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


def create_remediation(db: Session, description:str):
    remediation = models.Remediation(
        description = description,
        status = False
        )
    db.add(remediation)
    db.commit()
    db.refresh(remediation)
    return remediation


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

