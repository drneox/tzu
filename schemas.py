from typing import List
from uuid import UUID
from pydantic import BaseModel, FilePath
from datetime import datetime

class InformationSystemBase(BaseModel):
    title: str
    description: str | None = None
  

class InformationSystemBaseCreate(InformationSystemBase):
    pass


class InformationSystem(InformationSystemBase):
    id: UUID
    datetime: datetime
    diagram: str | None = None

    class Config:
        # le especificamos que será para uso de un ORM
        from_attributes = True
        # Colocamos un ejemplo que se mostrará en el SWAGGER

class UseCase(BaseModel):
    id: UUID
    title: str
    description:str
    information_system_id: str
    class Config:
        from_attributes = True

class Remediation(BaseModel):
    description: str
    status: bool = False


class Risk(BaseModel):
    damage: int
    reproducibility: int
    exploitability: int
    affected_users: int
    discoverability: int
    compliance: int


class Threat(BaseModel):
    id: UUID
    type: str
    title:str
    description:str
    remediation: Remediation
    risk: Risk
    class Config:
        from_attributes = True
  
class InformationSystem(InformationSystemBase):
    id: UUID
    datetime: datetime
    diagram: str | None = None
    threats: List[Threat] = []
    class Config:
        # le especificamos que será para uso de un ORM
        from_attributes = True
        # Colocamos un ejemplo que se mostrará en el SWAGGER




