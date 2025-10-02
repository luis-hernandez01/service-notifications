# tests/test_crud_credentials_services.py
from src.services.crud_credentials_services import (
    create_credential,
    get_credential_by_id,
    update_credential,
    delete_credential,
)
from src.schemas.crud_credentials_schema import CredentialsCreate, CredentialsUpdate


def test_create_get_update_delete_credential(db_session):
    payload = CredentialsCreate(
        identificador="cred-test",
        client_id="cid",
        client_secret="csecret",
        tenant_id="tid",
        username="user@example.com",
    )
    cred = create_credential(db_session, payload)
    assert cred.id is not None
    # get
    found = get_credential_by_id(db_session, cred.id)
    assert found.id == cred.id
    # update
    upd = CredentialsUpdate(client_id="newcid", client_secret="newsecret")
    updated = update_credential(db_session, cred.id, upd)
    assert updated.client_id == "newcid"
    # delete
    deleted = delete_credential(db_session, cred.id)
    assert deleted.activo == 2
