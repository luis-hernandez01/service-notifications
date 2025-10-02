# tests/test_crud_templates_services.py
import pytest
from src.services.crud_templates_services import (
    create_notification,
    get_template_by_id,
    update_notification,
    delete_notification,
)
from src.services.crud_credentials_services import create_credential
from src.schemas.crud_templates_schema import CreateNotification, UpdateNotification
from src.schemas.crud_credentials_schema import CredentialsCreate


def test_create_get_update_delete_template(db_session):
    # 1) create a credential (foreign key required by Plantillas)
    cred_payload = CredentialsCreate(
        identificador="test-cred",
        client_id="cid",
        client_secret="csecret",
        tenant_id="tenant",
        username="user@example.com",
    )
    cred_obj = create_credential(db_session, cred_payload)
    assert cred_obj.id is not None

    # 2) create a template
    tpl_payload = CreateNotification(
        identifying_name="tpl-1",
        description="plantilla de prueba",
        content_html="<p>Hola</p>",
        credenciales_id=cred_obj.id,
    )
    tpl_obj = create_notification(db_session, tpl_payload)
    assert tpl_obj.id is not None
    assert tpl_obj.identifying_name == "tpl-1"

    # 3) get by id
    got = get_template_by_id(tpl_obj.id, db_session)
    assert got is not None
    assert got.identifying_name == "tpl-1"

    # 4) update template
    upd_payload = UpdateNotification(
        identifying_name="tpl-1-upd",
        description="plantilla actualizada",
        content_html="<p>Hola actualizado</p>",
        credenciales_id=cred_obj.id,
    )
    updated = update_notification(tpl_obj.id, upd_payload, db_session)
    assert updated.identifying_name == "tpl-1-upd"

    # 5) delete (soft delete setting activo = 2)
    deleted = delete_notification(tpl_obj.id, db_session)
    assert deleted.activo == 2
