from fastapi import FastAPI
import uvicorn  
from src.routes.route import router
from contextlib import asynccontextmanager

from src.services.database_service import db_manager

from src.routes.route import router
from dotenv import load_dotenv
import os

load_dotenv(override=True)

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Starting application...")
    db_uri = os.getenv("DB_URI")
    print(f"DB_URI: {db_uri}")
    if db_uri:
        print("Initializing database...")
        db_manager.initialize(Connection_string=db_uri)
        print("Database initialized successfully")
    else:
        print("No DB_URI - skipping database initialization")

    yield
    print("Application shutting down...")

    if db_uri:
        db_manager.close()
        print('Database connections closed')



app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port = 8000)
