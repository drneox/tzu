# API endpoints for the Tzu application
import datetime
import shutil
import os
from uuid import UUID
from fastapi import FastAPI, HTTPException, Request, Depends, UploadFile, Body, status, Security, Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Importaciones locales
from . import models, schemas, crud, database, utils, init_db

# Inicializar la base de datos y crear usuario por defecto al arrancar
init_db.init_db()

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

# Configuración para OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para obtener la base de datos en cada solicitud
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para obtener el usuario actual a partir del token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Función para obtener usuario activo
async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

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
        # Threat Agent Factors
        skill_level=risk_data.get('skill_level', 0),
        motive=risk_data.get('motive', 0),
        opportunity=risk_data.get('opportunity', 0),
        size=risk_data.get('size', 0),
        # Vulnerability Factors
        ease_of_discovery=risk_data.get('ease_of_discovery', 0),
        ease_of_exploit=risk_data.get('ease_of_exploit', 0),
        awareness=risk_data.get('awareness', 0),
        intrusion_detection=risk_data.get('intrusion_detection', 0),
        # Technical Impact
        loss_of_confidentiality=risk_data.get('loss_of_confidentiality', 0),
        loss_of_integrity=risk_data.get('loss_of_integrity', 0),
        loss_of_availability=risk_data.get('loss_of_availability', 0),
        loss_of_accountability=risk_data.get('loss_of_accountability', 0),
        # Business Impact
        financial_damage=risk_data.get('financial_damage', 0),
        reputation_damage=risk_data.get('reputation_damage', 0),
        non_compliance=risk_data.get('non_compliance', 0),
        privacy_violation=risk_data.get('privacy_violation', 0)
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
    if db_information_system is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_information_system

@app.post("/evaluate/{information_system_id}")
async def evaluate(file: UploadFile, information_system_id: str, db: Session = Depends(database.get_db)):
    print("=== COMENZANDO EVALUACIÓN DE DIAGRAMA ===")
    
    try:
        # Guardar la imagen y obtener base64
        print(f"Procesando archivo: {file.filename}")
        image_b64 = save_image(file)
        db_information_system = crud.attach_diagram(db, information_system_id=information_system_id, image_path=file.filename)
        
        # Obtener análisis de la IA
        print("Llamando a clientAI...")
        result = clientAI(image_b64)
        print(f"Resultado de clientAI: tipo={type(result)}")
        
        # Verificar que el resultado sea un objeto con la propiedad 'threats'
        if isinstance(result, str):
            # Si es un string, es un error o mensaje
            print(f"El resultado es un string: '{result}'")
            return {"information_system": db_information_system, "message": "No se pudo analizar el diagrama correctamente", "success": False}
        
        # Verificar que tenga la propiedad threats y sea iterable
        print(f"¿Tiene propiedad threats? {hasattr(result, 'threats')}")
        if hasattr(result, 'threats'):
            print(f"Número de amenazas encontradas: {len(result.threats)}")
            print(f"Contenido de threats: {result.threats}")
        
        if not hasattr(result, 'threats') or not result.threats:
            print("No se encontraron amenazas o la propiedad no existe")
            return {"information_system": db_information_system, "message": "No se encontraron amenazas en el diagrama", "success": False}
            
        # Procesar las amenazas encontradas
        for i in result.threats:
            print(i)
            remediation = crud.create_remediation(db, i.remediation)
            risk = crud.create_risk(db, i.risk)
            threat = crud.create_threat(db, i.title, i.description, i.categories, UUID(information_system_id), risk.id, remediation.id)
        
        print(f"Se encontraron {len(result.threats)} amenazas")
        return {"information_system": db_information_system, "message": f"Se analizó el diagrama exitosamente y se encontraron {len(result.threats)} amenazas", "success": True}
    
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")
        return {"message": f"Error durante el procesamiento: {str(e)}", "success": False}


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

# Endpoints de autenticación
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user