"""Ponto de entrada da aplicação."""
import uvicorn
from src.infrastructure.config.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.interface.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
