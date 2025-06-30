from fastapi import Request
from app.external_service.ai import ai_service
from app.external_service.storage import storage_service

def get_process_pool(request: Request):
    """
    Retrieve the process pool from the request state.
    """
    return request.app.state.process_pool

def get_ai_service(request: Request):
    """
    Retrieve the AI service from the request state.
    """
    return ai_service

def get_storage_service(request: Request):
    """
    Retrieve the storage service from the request state.
    """
    return storage_service