from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.config.config import get_session
from src.schemas.crud_templates_schema import Notification, CreateNotification, UpdateNotification, NotificationOut
from src.services import crud_templates_services


# inicializacion del roter 
crud_templates_routes = APIRouter(prefix="/Crud", tags=["Plantillas"])


@crud_templates_routes.get("/templates", response_model=list[NotificationOut])
def  list_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    try: 
        return crud_templates_services.consult_notifications(db,skip=skip,limit=limit)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al listar plantilla de notificaciones: {str(e)}')

@crud_templates_routes.post("/templates", response_model=NotificationOut)
def create_notification(notification: CreateNotification, db: Session = Depends(get_session)):
    try:
        return crud_templates_services.create_notification(db, notification)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al crear plantilla de notificaciones: {str(e)}')

@crud_templates_routes.get("/templates/{id}", response_model=NotificationOut)
def read_notification(id_notification: int, db: Session = Depends(get_session)):
    try:
        obj = crud_templates_services.get_template_by_id(id_notification, db)
        if obj is None:
            raise HTTPException(status_code=404,detail=f"No se encontro plantilla de notificacion con el ID: {id}, por favor verifique la informacion")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al consultar template de notificaciones: {str(e)}')

@crud_templates_routes.patch("/templates/{id}",response_model=NotificationOut)
def update_notification(id_notification: int, data: UpdateNotification, db: Session = Depends(get_session)):
    try:
        return crud_templates_services.update_notification(id_notification, data, db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al actualizar credencial: {str(e)}')

@crud_templates_routes.delete("/templates/{id}", response_model=NotificationOut)
def delete_notification(id_notification: int, db: Session = Depends(get_session)):
    try:
        return crud_templates_services.delete_notification(id_notification, db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f'Error al eliminar credencial: {str(e)}')
