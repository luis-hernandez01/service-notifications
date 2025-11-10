from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

# from src.config.config import get_session
from ...config.config import get_session

from src.schemas.crud_credentials_schema import (
    CredentialsCreate,
    CredentialsOut,
    CredentialsUpdate,
    PaginacionSchema
)
from src.security.auth import verify_jwt_token
from src.services import crud_credentials_services as crud

# inicializacion del roter
router = APIRouter(prefix="/credenciales", tags=["Credenciales"])


@router.get("/credentials", response_model=PaginacionSchema)
def list_credentials(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo (true o false)"),
    
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
)-> Dict[str, Any]:
    skip = (page - 1) * per_page
    limit = per_page
    data = crud.list_credential(db, activo=activo, skip=skip, limit=limit)
    total = crud.count_credential(db, activo=activo)
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


@router.post("/credentials", response_model=CredentialsOut)
def create_credentials(
    data: CredentialsCreate,
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
):
    try:
        return crud.create_credential(db, data)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear credencial: {str(e)}"
        )


@router.get("/credentials/{id}", response_model=CredentialsOut)
def read_credentials_by_id(
    id: int, db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
):
    try:
        obj = crud.get_credential_by_id(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al consultar credencial: {str(e)}"
        )


@router.put("/credentials/{id}", response_model=CredentialsOut)
def update_credentials(
    id: int,
    data: CredentialsUpdate,
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
):
    try:
        obj = crud.update_credential(db, id, data)
        if not obj:
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar credencial: {str(e)}"
        )


@router.delete("/credentials/{id}", response_model=CredentialsOut)
def delete_credentials(
    id: int, db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
):
    try:
        obj = crud.delete_credential(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar credencial: {str(e)}"
        )
        
        
        
@router.post("/{id}/reactivate", response_model=CredentialsOut)
def reactivates(
    id: int, db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
):
    try:
        obj = crud.reactivate(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Credencial no encontrada")
        return obj
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al reactivar credencial: {str(e)}"
        )
        
@router.get("/{id}")        
def get_show(id: int, 
                db: Session = Depends(lambda: next(get_session(0))),
                tokenpayload: dict = Depends(verify_jwt_token)):
    return crud.show(db, id)