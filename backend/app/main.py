from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine, Base
from app import models
from app.routes import router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Cloud-Native Social Discussion Platform",
    description="Backend API for a social discussion platform",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix="/api")


@app.get("/")
def home():
    return {
        "message": "Cloud-Native Social Discussion Platform API is running!"
    }


@app.get("/test-db")
def test_database():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        return {
            "database": "connected",
            "result": result.scalar()
        }
