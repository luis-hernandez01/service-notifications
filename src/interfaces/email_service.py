from abc import ABC, abstractmethod
from src.models.smtp_model import EmailRequest

class IEmailService(ABC):
    """Interfaz base para servicios de envío de correos"""

    @abstractmethod
    async def send(self, req: EmailRequest) -> None:
        pass
