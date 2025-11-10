from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

from src.models.credenciales_model import CredencialesCorreo
from src.schemas.crud_credentials_schema import CredentialsCreate, CredentialsUpdate


def get_credential_by_id(db: Session, id: int):
    try:
        return (
            db.query(CredencialesCorreo)
            .filter(and_(CredencialesCorreo.activo == True, CredencialesCorreo.id == id))
            .first()
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al consultar por ID: {str(e)}"
        )



def list_credential(db: Session, skip: int, limit: int, activo: bool | None = None):
    return db.query(CredencialesCorreo).filter(CredencialesCorreo.activo == activo).offset(skip).limit(limit).all()
def count_credential(db: Session, activo: bool | None = None):
    return db.query(CredencialesCorreo).filter(CredencialesCorreo.activo == activo).count()


def create_credential(db: Session, data: CredentialsCreate):
    try:
        db_obj = CredencialesCorreo(**data.model_dump())
        db_obj.created_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error al crear credencial: {str(e)}"
        )


def update_credential(db: Session, id: int, data: CredentialsUpdate):
    try:
        obj = get_credential_by_id(db, id)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail="No se encontro ninguna credencial con el ID: {id}, por favor verifique la informacion",
            )
        for field, value in data.model_dump(exclude_unset=True).items():

            setattr(obj, field, value)
            obj.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar la credencial: {str(e)}"
        )


def delete_credential(db: Session, id: int):
    try:
        obj = get_credential_by_id(db, id)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail="No se encontro ninguna credencial con el ID: {id}, por favor verifique la informacion",
            )
        obj.deleted_at = datetime.utcnow()
        obj.activo = False  # 2 representa inactivo
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar la credencial: {str(e)}"
        )
        
        
        
def reactivate(db: Session, id: int):
    try:
        obj = db.query(CredencialesCorreo).filter(
            CredencialesCorreo.id == id).first()
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        print(obj.activo)
        if obj.activo:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="El registro ya se encuentra activo")
        
        obj.activo = True 
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar la credencial: {str(e)}"
        )

def show(db: Session, id: int):
        entity = db.query(CredencialesCorreo).filter(
            CredencialesCorreo.id == id,
                CredencialesCorreo.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        if id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo id se encuentra vacio ingresa un dato valido")
        return entity