import pytest
from src.models.smtp_model_basic import EmailRequest
from src.schemas.crud_templates_schema import CreateNotification
from pydantic import ValidationError


def test_email_request_accepts_dict_body_html():
    payload = {
        "subject": "Prueba",
        "body_html": {"titulo": "Hola"},
        "to": "dest@example.com",
        "identifying_name": "some_template",
    }
    req = EmailRequest(**payload)
    assert isinstance(req.body_html, dict)
    assert req.subject == "Prueba"


def test_create_notification_schema_validation():
    with pytest.raises(ValidationError):
        CreateNotification(
            identifying_name="",
            description="d",
            content_html="x",  # too short
            credenciales_id=1,
        )
