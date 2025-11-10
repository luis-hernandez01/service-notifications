from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from src.config.config import get_session
from src.schemas.crud_templates_schema import (
    CreateNotification,
    PaginacionSchema,
    UpdateNotification,
    NotificationOut
)
from src.security.auth import verify_jwt_token
from src.services import crud_templates_services

# inicializacion del roter
router = APIRouter(prefix="/plantilla", tags=["Plantillas"])


@router.get("/templates", response_model=PaginacionSchema)
def list_notifications(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo (true o false)"),
    
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
)-> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    
    data = crud_templates_services.list_template(db, activo=activo, skip=skip, limit=limit)
    total = crud_templates_services.count_template(db, activo=activo)
    # Método adicional para contar todos los datos
    return {
        "items": data,
        "per_page": per_page,
        "size": limit,
        "total": total,
        "last_page" : (total + per_page - 1) // per_page,
        "page": page,
        "pages": (total + limit - 1) // limit  # Redondeo hacia arriba
        
    }


@router.post("/templates", response_model=NotificationOut)
def create_notification(
    notification: CreateNotification,
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    try:
        return crud_templates_services.create_notification(db, notification)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="Error al crear plantilla de notificaciones: {str(e)}",
        )


@router.get("/templates/{id}")
def read_notification(
    id: int,
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    try:
        obj = crud_templates_services.get_template_by_id(id, db)
        if obj is None:
            raise HTTPException(
                status_code=404,
                detail="No se encontro plantilla de notificacion con el ID: {id}, por favor verifique la informacion",
            )
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar template de notificaciones: {str(e)}",
        )


@router.patch("/templates/{id}", response_model=NotificationOut)
def update_notification(
    id: int,
    data: UpdateNotification,
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    try:
        return crud_templates_services.update_notification(id, data, db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="Error al actualizar credencial: {str(e)}"
        )


@router.delete("/templates/{id}", response_model=NotificationOut)
def delete_notification(
    id_notification: int,
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token),
):
    try:
        return crud_templates_services.delete_notification(id_notification, db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="Error al eliminar la planntilla: {str(e)}"
        )


@router.post("/{id}/reactivate", response_model=NotificationOut)
def reactivates(
    id: int, db: Session = Depends(lambda: next(get_session(0))), 
    tokenpayload: dict = Depends(verify_jwt_token)
):
    try:
        obj = crud_templates_services.reactivate(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="plantilla no encontrada")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al reactivar la planntilla: {str(e)}"
        )
        
        
@router.get("/{id}")        
def get_show(id: int, 
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return crud_templates_services.show(db, id)