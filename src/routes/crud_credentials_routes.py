from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.schemas.crud_credentials_schema import CredentialsCreate, CredentialsUpdate, CredentialsOut
from src.services import crud_credentials_services as crud
from src.config.config import get_session


# inicializacion del roter 
crud_credentials_router = APIRouter(prefix="/Crud", tags=["Credenciales"])


@crud_credentials_router.get("/credentials", response_model=list[CredentialsOut])
def list_credentials(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    try:
        return crud.get_all_credentials(db, skip, limit)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al listar credenciales: {str(e)}')

@crud_credentials_router.post("/credentials", response_model=CredentialsOut)
def create_credentials(data: CredentialsCreate, db: Session = Depends(get_session)):
    try:
        return crud.create_credential(db, data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al crear credencial: {str(e)}')

@crud_credentials_router.get("/credentials/{id}", response_model=CredentialsOut)
def read_credentials_by_id(id: int, db: Session = Depends(get_session)):
    try:
        obj = crud.get_credential_by_id(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al consultar credencial: {str(e)}')

@crud_credentials_router.put("/credentials/{id}", response_model=CredentialsOut)
def update_credentials(id: int, data: CredentialsUpdate, db: Session = Depends(get_session)):
    try:
        obj = crud.update_credential(db, id, data)
        if not obj:
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al actualizar credencial: {str(e)}')

@crud_credentials_router.delete("/credentials/{id}", response_model=CredentialsOut)
def delete_credentials(id: int, db: Session = Depends(get_session)):
    try:
        obj = crud.delete_credential(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al eliminar credencial: {str(e)}')
