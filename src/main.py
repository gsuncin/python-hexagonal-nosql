from fastapi import FastAPI
from src.adapters.driving.api.routes import (
    router_auth,
    router_video,
    router_base,
)
from src.core import settings

app = FastAPI(
    title="Backend API",
    version="0.0.1",
    license_info={
        "name": "MIT",
    },
    debug=settings.DEBUG,
)

app.include_router(router_auth)
app.include_router(router_video)
app.include_router(router_base)
