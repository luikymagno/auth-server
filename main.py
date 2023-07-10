from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine

from auth_server.routes import oauth, management
from auth_server.auth_manager import manager as auth_manager
from auth_server.utils.scope_manager import OLTPScopeManager
from auth_server.utils.client_manager import OLTPClientManager
from auth_server.utils.constants import DATABASE_URL
from auth_server.utils import models
from auth_server.utils import exceptions

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
auth_manager.scope_manager = OLTPScopeManager(engine=engine)
auth_manager.client_manager = OLTPClientManager(engine=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(oauth.router)
app.include_router(management.router)

@app.exception_handler(exceptions.HTTPException)
async def unicorn_exception_handler(_: Request, exc: exceptions.HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code.value,
            "detail": exc.detail
        },
    )

@app.get("/")
async def index() -> str:
    return "index"
