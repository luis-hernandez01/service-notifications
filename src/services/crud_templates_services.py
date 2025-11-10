from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

from src.models.plantilla_model import Plantillas
from src.schemas.crud_templates_schema import CreateNotification, UpdateNotification


def get_template_by_id(id: int, db: Session):
    try:
        return (
            db.query(Plantillas)
            .filter(and_(Plantillas.activo == True, Plantillas.id == id))
            .first()
        )  # filter(Plantillas.id == id_notification).first()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar plantilla de notificaciones por ID: {str(e)}",
        )

def list_template(db: Session, skip: int, limit: int, activo: bool | None = None):
    return db.query(Plantillas).filter(Plantillas.activo == activo).offset(skip).limit(limit).all()
def count_template(db: Session, activo: bool | None = None):
    return db.query(Plantillas).filter(Plantillas.activo == activo).count()

def create_notification(db: Session, notification: CreateNotification):
    try:
        datacreate = db.query(Plantillas).filter(
            Plantillas.identifying_name == notification.identifying_name,
                Plantillas.activo == True).first()
        if datacreate:
            raise HTTPException(
                status_code=400, 
                detail="El nombre identificador ya existe en otro registro",
                )
        
        if len(notification.content_html) < 2:
            raise HTTPException(
                status_code=400,
                detail="El campo de contenido html debe tener un minimo de 2 caracteres",
            )
        
        if not notification.credenciales_id or str(notification.credenciales_id).strip() == "0":
            raise HTTPException(
                status_code=400,
                detail="El campo credenciales_id requiere un valor diferente a 0 o vacio",
            )
            
        db_notification = Plantillas(**notification.model_dump())
        db_notification.created_at = datetime.utcnow()
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al crear la plantilla de notificación: {str(e)}",
        )


def update_notification(id: int, data: UpdateNotification, db: Session):
    try:
        
        
        
        if data.identifying_name:
            existe = (
                db.query(Plantillas)
                .filter(Plantillas.identifying_name == data.identifying_name, Plantillas.id != id)
                .first()
            )
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El identificador '{data.identifying_name}' ya está siendo usado por otro registro.",
                )
        
        
        notification = get_template_by_id(id, db)
        if notification is None:
            raise HTTPException(
                status_code=404,
                detail="No se encontro notificacion con el ID: {id}, por favor verifique la informacion",
            )
        
        if len(data.content_html) < 2:
            raise HTTPException(
                status_code=400,
                detail="El campo de contenido html debe tener un minimo de 2 caracteres",
            )
        
        if not data.credenciales_id or str(notification.credenciales_id).strip() == "0":
            raise HTTPException(
                status_code=400,
                detail="El campo credenciales_id requiere un valor diferente a 0 o vacio",
            )
            
        data_dict = data.model_dump()
        for campo, valor in data_dict.items():
            setattr(notification, campo, valor)
            notification.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(notification)
        return notification
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error interno al editar la plantilla de notificación: {str(e)}",
        )


def delete_notification(id_notification: int, db: Session):
    try:
        notification = (
            db.query(Plantillas).filter(Plantillas.id == id_notification).first()
        )
        if notification is None:
            raise HTTPException(
                status_code=404,
                detail="No se encontro plantilla de notificacion con el ID: {id}, por favor verifique la informacion",
            )
        notification.deleted_at = datetime.utcnow()
        notification.activo = False
        db.commit()
        db.refresh(notification)
        return notification
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al eliminar la plantilla de notificación: {str(e)}",
        )


def reactivate(db: Session, id: int):
    try:
        obj = db.query(Plantillas).filter(
            Plantillas.id == id).first()
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
            status_code=500, detail=f"Error al eliminar la plantilla: {str(e)}"
        )

def show(db: Session, id: int):
        entity = db.query(Plantillas).filter(
            Plantillas.id == id,
                Plantillas.activo == True).first()
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El registro no fue hallada")
        if id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo id se encuentra vacio ingresa un dato valido")
        return entity