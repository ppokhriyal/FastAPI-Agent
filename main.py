from fastapi import FastAPI
from registration.routes import device_registration_router
from sync.routes import sync_info_router
from config.api_info import ProjectInfo


def include_routes(app):
    app.include_router(device_registration_router)
    app.include_router(sync_info_router)

def start_api():
    app = FastAPI(title=ProjectInfo.PROJECT_NAME, version=ProjectInfo.PROJECT_VERSION)
    include_routes(app)
    return app

app = start_api()