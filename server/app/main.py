from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.database import SessionLocal, engine
from app.core.seed import seed_tea_types
from app.models import Base
from app.routers.auth import router as auth_router
from app.routers.recipes import router as recipe_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_tea_types(db)
    yield


app = FastAPI(title="TeaGuardian API", version="1.0.0", lifespan=lifespan)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(auth_router)
app.include_router(recipe_router)
