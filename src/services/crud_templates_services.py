from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from src.models.plantilla_model import Plantillas
from src.schemas.crud_templates_schema import CreateNotification,UpdateNotification

def get_template_by_id(id: int, db: Session):
    try:
        return db.query(Plantillas).filter(and_(Plantillas.activo == 1,Plantillas.id == id)).first()#filter(Plantillas.id == id_notification).first()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error al consultar plantilla de notificaciones por ID: {str(e)}'
        )

def consult_notifications(db: Session,skip: int = 0, limit: int = 10):
    try:
        return db.query(Plantillas).filter(Plantillas.activo == 1).offset(skip).limit(limit).all()
    except SQLAlchemyError as e: 
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al consultar las plantillas de notificacies: {str(e)}"
        )

def create_notification(db: Session, notification: CreateNotification):
    try:
        db_notification = Plantillas(**notification.dict())
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    except SQLAlchemyError as e: 
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al crear la plantilla de notificación: {str(e)}"
        )

def update_notification(id: int, data: UpdateNotification , db: Session):
    try:
        notification = get_template_by_id(id,db)
        if notification is None:
            raise HTTPException(status_code=404,detail=f"No se encontro notificacion con el ID: {id}, por favor verifique la informacion")
        data_dict = data.dict(exclude_unset=True)
        for campo, valor in data_dict.items():
            setattr(notification,campo,valor)
        db.commit()
        db.refresh(notification)
        return notification
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al editar la plantilla de notificación: {str(e)}"
        )

def delete_notification(id_notification: int, db: Session):
    try:
        notification = db.query(Plantillas).filter(Plantillas.id == id_notification).first()
        if notification is None:
            raise HTTPException(status_code=404,detail=f"No se encontro plantilla de notificacion con el ID: {id}, por favor verifique la informacion")
        notification.activo = 2 # 2 representa inactivo
        db.commit()
        db.refresh(notification)
        return notification
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno al eliminar la plantilla de notificación: {str(e)}")

