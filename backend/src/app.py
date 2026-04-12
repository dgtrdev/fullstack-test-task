from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.alerts import router as alerts_router
from src.api.files import router as files_router
from src.settings import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(files_router)
app.include_router(alerts_router)
