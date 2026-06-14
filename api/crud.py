from uuid import UUID
import json
import models
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, text
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
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
    
    # Exclude threats from archived systems
    query = query.join(models.InformationSystem).filter(models.InformationSystem.archived == False)

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
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # Default 24 hours (Decision 6)

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def list_users(db: Session, skip: int = 0, limit: int = 100, role: str = None, is_active: bool = None):
    query = db.query(models.User)
    if role is not None:
        query = query.filter(models.User.role == role)
    if is_active is not None:
        query = query.filter(models.User.is_active == is_active)
    return query.offset(skip).limit(limit).all()

def _count_active_admins(db: Session) -> int:
    return db.query(models.User).filter(
        models.User.role == "admin",
        models.User.is_active == True
    ).count()

def update_user_role(db: Session, user_id: str, new_role: str, performed_by_id: str = None):
    user = db.query(models.User).filter(models.User.id == UUID(str(user_id))).first()
    if not user:
        return None, "User not found"
    # RB-001: cannot demote the last active admin
    if user.role == "admin" and new_role != "admin":
        if _count_active_admins(db) <= 1:
            return None, "Cannot demote the last active admin"
    old_role = user.role
    user.role = new_role
    # Keep is_admin in sync
    user.is_admin = (new_role == "admin")
    db.commit()
    db.refresh(user)
    if performed_by_id:
        create_audit_log_entry(
            db,
            action="update_user_role",
            target_user_id=str(user.id),
            performed_by_id=str(performed_by_id),
            detail=f"Changed role of '{user.username}' from '{old_role}' to '{new_role}'"
        )
    return user, None

def update_user_active(db: Session, user_id: str, is_active: bool, performed_by_id: str = None):
    user = db.query(models.User).filter(models.User.id == UUID(str(user_id))).first()
    if not user:
        return None, "User not found"
    # RB-002: cannot deactivate the last active admin
    if user.role == "admin" and not is_active:
        if _count_active_admins(db) <= 1:
            return None, "Cannot deactivate the last active admin"
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    if performed_by_id:
        create_audit_log_entry(
            db,
            action="update_user_active",
            target_user_id=str(user.id),
            performed_by_id=str(performed_by_id),
            detail=f"Set is_active={is_active} for user '{user.username}'"
        )
    return user, None

def delete_user(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.id == UUID(str(user_id))).first()
    if not user:
        return None, "User not found"
    # RB-003: cannot delete the last active admin
    if user.role == "admin" and user.is_active:
        if _count_active_admins(db) <= 1:
            return False, "Cannot delete the last active admin"
    db.delete(user)
    db.commit()
    return True, None


def check_delete_permission(resource, current_user: models.User) -> bool:
    """
    Check if current_user can delete the given resource (RB-006, Decision 8).
    - Admin can always delete.
    - Analyst can delete only resources they created (created_by == current_user.id).
    Returns True if allowed, False otherwise.
    """
    if current_user.role == "admin":
        return True
    if current_user.role == "analyst":
        if resource.created_by is None:
            return False
        return str(resource.created_by) == str(current_user.id)
    return False


def create_audit_log_entry(db: Session, action: str, performed_by_id: str, target_user_id: str = None, detail: str = None):
    """Create an audit log entry for administrative actions (FR-011)."""
    import datetime as dt
    import uuid as _uuid
    entry = models.AuditLog(
        action=action,
        target_user_id=_uuid.UUID(str(target_user_id)) if target_user_id else None,
        performed_by_id=_uuid.UUID(str(performed_by_id)),
        timestamp=dt.datetime.utcnow(),
        detail=detail
    )
    db.add(entry)
    db.commit()
    return entry


def list_audit_log(db: Session, skip: int = 0, limit: int = 100, action: str = None, target_user_id: str = None):
    """List audit log entries with optional filters."""
    query = db.query(models.AuditLog)
    if action:
        query = query.filter(models.AuditLog.action == action)
    if target_user_id:
        query = query.filter(models.AuditLog.target_user_id == target_user_id)
    return query.order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate, is_admin: bool = False, performed_by_id=None):
    hashed_password = get_password_hash(user.password)
    role = user.role if hasattr(user, 'role') and user.role else ("admin" if is_admin else "reader")
    db_user = models.User(
        username=user.username,
        email=user.email,
        name=user.name,
        password_hash=hashed_password,
        is_active=True,
        is_admin=(role == "admin"),
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if performed_by_id:
        create_audit_log_entry(
            db,
            action="create_user",
            target_user_id=str(db_user.id),
            performed_by_id=str(performed_by_id),
            detail=f"Created user '{db_user.username}' with role '{role}'"
        )
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
                inherent_score = risk.overall_risk_score
                clamped = min(float(data[key]), inherent_score) if data[key] is not None else None
                print(f"Guardando riesgo residual: {data[key]} → {clamped} (inherente: {inherent_score})")
                setattr(risk, key, clamped)
            else:
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

def get_information_systems(db: Session, skip: int = 0, limit: int = 100, project_id: Optional[UUID] = None, include_archived: bool = False):
    query = db.query(models.InformationSystem)
    if not include_archived:
        query = query.filter(models.InformationSystem.archived == False)
    if project_id is not None:
        query = query.filter(models.InformationSystem.project_id == project_id)
    return query.order_by(models.InformationSystem.datetime.desc()).offset(skip).limit(limit).all()
 
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
 
def create_information_system(db: Session, information_system: schemas.InformationSystemCreate, created_by=None):
    project_id = information_system.project_id
    # If project_name is provided (and no project_id), always create a new project
    if information_system.project_name and not project_id:
        if created_by is None:
            raise ValueError("created_by is required when project_name is provided")
        new_project = create_project_by_name(
            db,
            name=information_system.project_name,
            created_by=created_by
        )
        project_id = new_project.id

    db_information_system = models.InformationSystem(
        title=information_system.title,
        description=information_system.description,
        created_by=created_by,
        project_id=project_id,
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


def attach_diagram(db: Session, information_system_id: str, image_path: str, input_type: str = None):
    information_system = db.query(models.InformationSystem).filter(models.InformationSystem.id==UUID(information_system_id)).first()
    information_system.diagram = image_path
    if input_type is not None:
        information_system.diagram_input_type = input_type
    db.add(information_system)
    db.commit()
    db.refresh(information_system)
    return information_system

def create_threat(db: Session, title:str, description:str, type:str, information_system_id: str, risk_id:str, remediation_id:str, created_by=None):
    threat = models.Threat(
        information_system_id=information_system_id,
        remediation_id= remediation_id,
        risk_id=risk_id,
        description=description,
        title=title,
        type=type,
        created_by=created_by,
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


def create_remediation(db: Session, description: str, control_tags: list = None, created_by=None):
    # Convertir lista de control_tags a JSON string
    control_tags_json = json.dumps(control_tags) if control_tags else "[]"
    
    remediation = models.Remediation(
        description=description,
        status=False,
        control_tags=control_tags_json,
        created_by=created_by
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
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Keep claims aligned with decode expectations in api.get_current_user
    to_encode.update({
        "exp": expire,
        "iat": now,
        "nbf": now,
        "iss": "tzu-api",
        "aud": "tzu-client",
    })
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



# =====================================================
# PROJECT CRUD FUNCTIONS
# =====================================================

def create_project(db: Session, project: schemas.ProjectCreate, created_by) -> models.Project:
    db_project = models.Project(
        name=project.name.strip(),
        description=project.description,
        created_by=created_by,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def create_project_by_name(db: Session, name: str, created_by) -> models.Project:
    """Always creates a new project with the given name (no lookup). See research.md Decision 4."""
    db_project = models.Project(
        name=name.strip(),
        created_by=created_by,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    from sqlalchemy import func, select
    analysis_count_sub = (
        select(func.count())
        .where(models.InformationSystem.project_id == models.Project.id)
        .correlate(models.Project)
        .scalar_subquery()
    )
    member_count_sub = (
        select(func.count())
        .where(models.ProjectMember.project_id == models.Project.id)
        .correlate(models.Project)
        .scalar_subquery()
    )
    rows = (
        db.query(
            models.Project,
            analysis_count_sub.label("analysis_count"),
            member_count_sub.label("member_count"),
        )
        .order_by(models.Project.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    results = []
    for project, ac, mc in rows:
        project._analysis_count = ac
        project._member_count = mc
        results.append(project)
    return results


def get_project(db: Session, project_id) -> Optional[models.Project]:
    from sqlalchemy import func, select
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        return None
    project._analysis_count = db.query(models.InformationSystem).filter(
        models.InformationSystem.project_id == project_id
    ).count()
    project._member_count = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id
    ).count()
    return project


def update_project(db: Session, project_id, data: schemas.ProjectUpdate, current_user: models.User) -> Optional[models.Project]:
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        return None, "not_found"
    if str(project.created_by) != str(current_user.id) and current_user.role != "admin":
        return None, "forbidden"
    if data.name is not None:
        name = data.name.strip()
        if not name:
            return None, "empty_name"
        project.name = name
    if data.description is not None:
        project.description = data.description
    db.commit()
    db.refresh(project)
    return project, None


def delete_project(db: Session, project_id, current_user: models.User):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        return False, "not_found"
    if str(project.created_by) != str(current_user.id) and current_user.role != "admin":
        return False, "forbidden"
    db.delete(project)
    db.commit()
    return True, None


def update_information_system(db: Session, information_system_id: str, data: schemas.InformationSystemUpdate, current_user: models.User):
    system = db.query(models.InformationSystem).filter(
        models.InformationSystem.id == UUID(information_system_id)
    ).first()
    if system is None:
        return None, "not_found"
    if str(system.created_by) != str(current_user.id) and current_user.role != "admin":
        return None, "forbidden"
    if data.title is not None:
        system.title = data.title
    if data.description is not None:
        system.description = data.description
    if data.project_name_inline:
        new_project = create_project_by_name(db, name=data.project_name_inline, created_by=current_user.id)
        system.project_id = new_project.id
    elif "project_id" in data.model_fields_set:
        system.project_id = data.project_id
    db.commit()
    db.refresh(system)
    return system, None


# =====================================================
# PROJECT MEMBER CRUD FUNCTIONS
# =====================================================

def get_project_members(db: Session, project_id, current_user: models.User):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        return None, "not_found"
    if str(project.created_by) != str(current_user.id) and current_user.role != "admin":
        return None, "forbidden"
    members = (
        db.query(models.ProjectMember, models.User)
        .join(models.User, models.User.id == models.ProjectMember.user_id)
        .filter(models.ProjectMember.project_id == project_id)
        .all()
    )
    result = []
    for membership, user in members:
        result.append({
            "user_id": user.id,
            "username": user.username,
            "name": user.name,
            "role": user.role,
            "added_at": membership.added_at,
            "added_by": membership.added_by,
        })
    return result, None


def add_project_member(db: Session, project_id, user_id, added_by, current_user: models.User):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        return None, "not_found"
    if str(project.created_by) != str(current_user.id) and current_user.role != "admin":
        return None, "forbidden"
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if target_user is None:
        return None, "user_not_found"
    existing = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.user_id == user_id,
    ).first()
    if existing:
        return None, "already_member"
    membership = models.ProjectMember(
        project_id=project_id,
        user_id=user_id,
        added_by=added_by,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return {
        "user_id": target_user.id,
        "username": target_user.username,
        "name": target_user.name,
        "role": target_user.role,
        "added_at": membership.added_at,
        "added_by": membership.added_by,
    }, None


def remove_project_member(db: Session, project_id, user_id, current_user: models.User):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        return False, "not_found"
    if str(project.created_by) != str(current_user.id) and current_user.role != "admin":
        return False, "forbidden"
    membership = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.user_id == user_id,
    ).first()
    if membership is None:
        return False, "not_found"
    db.delete(membership)
    db.commit()
    return True, None
