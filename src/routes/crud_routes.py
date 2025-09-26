from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.config import get_session
from src.models.crud_model import Notification, CreateNotification, UpdateNotification
from src.services import crud_services


# inicializacion del roter 
crud_routes = APIRouter()



@crud_routes.get("/notifications/", response_model=list[Notification])
def  list_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    return crud_services.consult_notifications(db,skip=skip,limit=limit)

@crud_routes.post("/notifications/", response_model=Notification)
def create_notification(notification: CreateNotification, db: Session = Depends(get_session)):
    return crud_services.create_notification(db, notification)

@crud_routes.get("/notifications/{id}", response_model=Notification)
def read_notification(id_notification: int, db: Session = Depends(get_session)):
    return crud_services.read_notification(id_notification, db)

@crud_routes.patch("/notifications/{id}",response_model=UpdateNotification)
def update_notification(id_notification: int, data: UpdateNotification, db: Session = Depends(get_session)):
    return crud_services.update_notification(id_notification, data, db)

@crud_routes.delete("/notifications/{id}")
def delete_notification(id_notification: int, db: Session = Depends(get_session)):
    return crud_services.delete_notification(id_notification, db)