from uuid import UUID
from . import models
from sqlalchemy.orm import Session, joinedload

from . import schemas

def update_threat_risk(db: Session, threat_id: str, data: dict):
    threat = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.id == UUID(threat_id)).first()
    if not threat:
        return None
    risk = db.query(models.Risk).filter(models.Risk.id == threat.risk_id).first()
    remediation = db.query(models.Remediation).filter(models.Remediation.id == threat.remediation_id).first()
    # Actualizar campos de Threat
    for key in ['title', 'type', 'description']:
        if key in data:
            print(f"Actualizando Threat {key}: {getattr(threat, key)} -> {data[key]}")
            setattr(threat, key, data[key])
    # Actualizar campo de Remediation
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
    # Actualizar campos de Risk
    for key in ['damage', 'reproducibility', 'exploitability', 'affected_users', 'discoverability', 'compliance']:
        if key in data and risk:
            print(f"Actualizando Risk {key}: {getattr(risk, key)} -> {data[key]}")
            setattr(risk, key, data[key])
    db.add(threat)
    if risk:
        db.add(risk)
    db.commit()
    db.refresh(threat)
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
        damage = risk.damage,
        reproducibility= risk.reproducibility,
        exploitability= risk.exploitability,
        affected_users= risk.affected_users,
        discoverability= risk.discoverability,
        compliance= risk.compliance,
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


