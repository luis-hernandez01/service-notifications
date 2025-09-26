from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.crud_credentials_schema import CredentialsCreate, CredentialsUpdate, CredentialsOut
from src.services import crud_credentials_services as crud
from src.config.config import get_session

crud_credentials_router = APIRouter(prefix="/credenciales", tags=["Credenciales"])


@crud_credentials_router.get("/credentials", response_model=list[CredentialsOut])
def list_credentials(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud.get_all_credentials(db, skip, limit)


@crud_credentials_router.post("/credentials", response_model=CredentialsOut)
def create_credentials(data: CredentialsCreate, db: Session = Depends(get_session)):
    return crud.create_credential(db, data)

@crud_credentials_router.get("/credentials/{id}", response_model=CredentialsOut)
def read_credentials_by_id(id: int, db: Session = Depends(get_session)):
    obj = crud.get_credential_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Credencial no encontrada")
    return obj

@crud_credentials_router.put("/credentials/{id}", response_model=CredentialsOut)
def update_credentials(id: int, data: CredentialsUpdate, db: Session = Depends(get_session)):
    obj = crud.update_credential(db, id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Credencial no encontrada")
    return obj

@crud_credentials_router.delete("/credentials/{id}", response_model=CredentialsOut)
def delete_credentials(id: int, db: Session = Depends(get_session)):
    obj = crud.delete_credential(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Credencial no encontrada")
    return obj