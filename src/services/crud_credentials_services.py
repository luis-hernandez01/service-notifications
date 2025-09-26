from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.credenciales_model import CredencialesCorreo
from src.schemas.crud_credentials_schema import CredentialsCreate, CredentialsUpdate

def get_credential_by_id(db: Session, id: int):
    try:
        return db.query(CredencialesCorreo).filter(and_(CredencialesCorreo.activo == 1,CredencialesCorreo.id == id)).first()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, 
            detail=f'Error al consultar por ID: {str(e)}'
        )

def get_all_credentials(db: Session, skip: int = 0, limit: int = 100):
    try: 
        return db.query(CredencialesCorreo).filter(CredencialesCorreo.activo == 1).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al listar credenciales: {str(e)}')

def create_credential(db: Session, data: CredentialsCreate):
    try: 
        db_obj = CredencialesCorreo(**data.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error al crear credencial: {str(e)}')

def update_credential(db: Session, id: int, data: CredentialsUpdate):
    try:
        obj = get_credential_by_id(db, id)
        if not obj:
            raise HTTPException(status_code=404,detail=f"No se encontro ninguna credencial con el ID: {id}, por favor verifique la informacion")
        for field, value in data.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error al actualizar la credencial: {str(e)}')

def delete_credential(db: Session, id: int):
    try:
        obj = get_credential_by_id(db, id)
        if not obj:
            raise HTTPException(status_code=404,detail=f"No se encontro ninguna credencial con el ID: {id}, por favor verifique la informacion")
        obj.activo = 2 # 2 representa inactivo
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error al eliminar la credencial: {str(e)}')

