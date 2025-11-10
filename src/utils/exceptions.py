"""
Excepciones personalizadas del proyecto.

@autor: Fabio Garcia
@fecha: Septiembre 2025
"""

class StorageError(Exception):
    """
    Excepción personalizada para errores relacionados con el almacenamiento.
    
    Esta excepción se utiliza para encapsular errores específicos que ocurren
    durante las operaciones con Azure Storage, proporcionando mensajes claros
    y contextuales.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
