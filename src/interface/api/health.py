"""Endpoint de health check."""
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class HealthResponse(BaseModel):
    """Resposta do health check."""
    status: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Verifica o status da API.
    
    Returns:
        HealthResponse: Status da aplicação
    """
    return HealthResponse(
        status="healthy",
        version="0.1.0"
    )
