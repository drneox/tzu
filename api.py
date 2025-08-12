# Endpoint para eliminar una amenaza por su id
from fastapi import Path


import datetime
import shutil
from uuid import UUID
from fastapi import FastAPI, HTTPException, Request, Depends, UploadFile, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import datetime
from typing import List

from .tzu_ai import clientAI
from .utils import save_image
from . import crud, models, schemas, database

app = FastAPI()
origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/diagrams", StaticFiles(directory="diagrams"), name="diagrams")

models.Base.metadata.create_all(bind=database.engine)

# Endpoint batch para actualizar los valores de riesgo de varias amenazas a la vez
class ThreatRiskUpdate(BaseModel):
    threat_id: str
    risk: dict


@app.get("/information_systems/{information_system_id}/threats", response_model=list[schemas.Threat])
async def get_threats_by_system(
    information_system_id: str,
    db: Session = Depends(database.get_db)
):
    try:
        system_uuid = UUID(information_system_id)
    except Exception:
        raise HTTPException(status_code=400, detail="El id del sistema no es un UUID válido")
    
    threats = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.information_system_id == system_uuid).all()
    return threats

@app.get("/threat/{threat_id}", response_model=schemas.Threat)
async def get_threat(
    threat_id: str = Path(...),
    db: Session = Depends(database.get_db)
):
    try:
        uuid_id = UUID(threat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="El id no es un UUID válido")
    
    threat = db.query(models.Threat).filter(models.Threat.id == uuid_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

@app.delete("/threat/{threat_id}")
async def delete_threat(
    threat_id: str = Path(...),
    db: Session = Depends(database.get_db)
):
    try:
        uuid_id = UUID(threat_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="El id no es un UUID válido")
    
    threat = db.query(models.Threat).filter(models.Threat.id == uuid_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    db.delete(threat)
    db.commit()
    return {"message": "Threat eliminado correctamente", "status": "success", "id": str(uuid_id)}


# Endpoint para actualizar los valores de riesgo de una amenaza
@app.put("/threat/{threat_id}/risk", response_model=schemas.Threat)
async def update_threat_risk(
    threat_id: str,
    risk: dict = Body(...),
    db: Session = Depends(database.get_db)
):
    updated_threat = crud.update_threat_risk(db, threat_id, risk)
    if not updated_threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return updated_threat

@app.post("/information_systems/{information_system_id}/threats", response_model=schemas.Threat)
async def create_threat_for_system(
    information_system_id: str,
    threat_data: dict = Body(...),
    db: Session = Depends(database.get_db)
):
    try:
        system_uuid = UUID(information_system_id)
    except Exception:
        raise HTTPException(status_code=400, detail="El id del sistema no es un UUID válido")
    
    # Verificar que el sistema existe
    system = db.query(models.InformationSystem).filter(models.InformationSystem.id == system_uuid).first()
    if not system:
        raise HTTPException(status_code=404, detail="Information System not found")
    
    # Crear risk
    risk_data = threat_data.get('risk', {})
    risk = crud.create_risk(db, schemas.Risk(
        damage=risk_data.get('damage', 1),
        reproducibility=risk_data.get('reproducibility', 1),
        exploitability=risk_data.get('exploitability', 1),
        affected_users=risk_data.get('affected_users', 1),
        discoverability=risk_data.get('discoverability', 1),
        compliance=risk_data.get('compliance', 1)
    ))
    
    # Crear remediation
    remediation_data = threat_data.get('remediation', {})
    remediation = crud.create_remediation(db, remediation_data.get('description', ''))
    
    # Crear threat
    threat = crud.create_threat(
        db,
        title=threat_data.get('title', 'Nueva Amenaza'),
        description=threat_data.get('description', ''),
        type=threat_data.get('type', 'Spoofing'),
        information_system_id=system_uuid,
        risk_id=risk.id,
        remediation_id=remediation.id
    )
    
    # Hacer eager loading del threat creado
    created_threat = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.id == threat.id).first()
    
    return created_threat

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, con):
  return templates.TemplateResponse(
        request=request, name="item.html")

@app.get("/information_systems/", response_model=list[schemas.InformationSystem])
async def read_information_systems(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    information_systems = crud.get_information_systems(db, skip=skip, limit=limit)
    return information_systems

@app.get("/information_systems/{information_system_id}", response_model=schemas.InformationSystem)
async def read_information_system(information_system_id: str, db: Session = Depends(database.get_db)):
    db_information_system = crud.get_information_system(db, information_system_id=information_system_id)
    print("xxx")
    print(db_information_system)
    if db_information_system is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_information_system

@app.post("/evaluate/{information_system_id}", response_model=schemas.InformationSystem)
async def evaluate(file: UploadFile, information_system_id: str,db: Session = Depends(database.get_db)):
    image_b64 = save_image(file)
    db_information_system = crud.attach_diagram(db, information_system_id=information_system_id, image_path=file.filename)
    result = clientAI(image_b64)
    for i in result.threats:
        print(i)
        remediation = crud.create_remediation(db, i.remediation)
        risk = crud.create_risk(db,i.risk)
        threat = crud.create_threat(db,i.title, i.description, i.categories, UUID(information_system_id), risk.id, remediation.id )
    print(result.threats)
    return db_information_system


@app.post("/new/", response_model=schemas.InformationSystem)
async def evaluate(information_system:schemas.InformationSystemBaseCreate, db: Session = Depends(database.get_db)):
    db_information_system = crud.create_information_system(db, information_system=information_system)
    return db_information_system

#    result = clientAI(item)
#    print(result.content)
#    return JSONResponse(content=result.content)

# Endpoint para actualizar los riesgos de todas las amenazas asociadas a un information_system_id
@app.put("/information_systems/{information_system_id}/threats/risk/batch", response_model=list[schemas.Threat])
async def update_threats_risk_by_system(
    information_system_id: str,
    risks: list = Body(...),
    db: Session = Depends(database.get_db)
):
    # Convertir el id a UUID
    try:
        system_uuid = UUID(information_system_id)
    except Exception:
        raise HTTPException(status_code=400, detail="El id del sistema no es un UUID válido")

    # Validar formato del payload
    print(f"Payload recibido en batch: {risks}")
    if not isinstance(risks, list):
        raise HTTPException(status_code=400, detail="El payload debe ser una lista de objetos con threat_id y campos de riesgo")
    for r in risks:
        if not isinstance(r, dict) or 'threat_id' not in r:
            raise HTTPException(status_code=400, detail="Cada objeto debe tener la clave 'threat_id'")

    # Filtrar threats usando el UUID correctamente
    threats = db.query(models.Threat).options(
        joinedload(models.Threat.risk),
        joinedload(models.Threat.remediation)
    ).filter(models.Threat.information_system_id == system_uuid).all()
    threats_by_id = {str(threat.id): threat for threat in threats}

    updated_threats = []
    for risk_update in risks:
        threat_id = str(risk_update.get('threat_id'))
        risk_data = risk_update.copy()
        risk_data.pop('threat_id', None)
        threat = threats_by_id.get(threat_id)
        if not threat:
            print(f"Amenaza con id {threat_id} no encontrada en el sistema {system_uuid}")
            continue
        updated = crud.update_threat_risk(db, threat_id, risk_data)
        if updated:
            updated_threats.append(updated)

    if not updated_threats:
        raise HTTPException(status_code=404, detail="No threats updated")
    return updated_threats