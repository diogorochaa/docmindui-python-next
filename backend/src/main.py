from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.error_handlers import register_exception_handlers
from src.modules.ai.routes import router as ai_router
from src.modules.auth.routes import router as auth_router
from src.modules.documents.routes import router as upload_router
from src.modules.health.routes import router as health_router
from src.modules.messages.routes import router as messages_router

app = FastAPI()
register_exception_handlers(app)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(ai_router)
app.include_router(upload_router)
app.include_router(messages_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois restringe
    # Com origem curinga, credenciais devem ficar desativadas (regra do CORS).
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
