# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.db import Base, engine
from app.api.auth import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield 


# init
app = FastAPI(
    title="AURA",
    description="Academic Unified Response Assistent",
    version="0.0.1",
    lifespan=lifespan
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend development ports
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)


# include api modules
app.include_router(auth_router, prefix='/api', tags=['Auth'])



@app.get("/")
def read_root():
    '''
        welcome message route
    '''
    return {"message": "Welcome to the FastAPI + LangChain + LangGraph project!"}