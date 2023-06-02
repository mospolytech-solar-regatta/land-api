from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.LandAPI import LandAPI
from app.LandAPI import set_app
from app.config.config import Config
from background.listener import create_listener, get_listener
from store.migrator import AlembicMigrator

api = FastAPI()


@api.on_event("startup")
async def startup_event():
    app = LandAPI(Config())
    set_app(app)
    origins = app.config.allow_origin
    # migrator = AlembicMigrator()
    # migrator.migrate_to_latest()
    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    listener = create_listener()
    await listener.listen()


@api.on_event("shutdown")
async def shutdown_event():
    await get_listener().stop()


@api.get("/")
async def root():
    return {}
