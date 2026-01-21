"""Configuração e inicialização da aplicação FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..webhooks import whatsapp, instagram, twitter
from . import health


def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.
    
    Returns:
        FastAPI: Aplicação configurada
    """
    app = FastAPI(
        title="CICNA Middleware",
        description="Middleware modular para conexão entre Typebot e plataformas de mensagens",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configuração de CORS
    # IMPORTANTE: Em produção, configurar origens específicas
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Substituir por origens específicas em produção
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Inclusão de routers
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(whatsapp.router, prefix="/api/v1/webhook", tags=["WhatsApp"])
    app.include_router(instagram.router, prefix="/api/v1/webhook", tags=["Instagram"])
    app.include_router(twitter.router, prefix="/api/v1/webhook", tags=["Twitter"])
    
    return app


app = create_app()
