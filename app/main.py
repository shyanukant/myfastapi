from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .database import engine
# from . import models
from .routers.posts import router as post_router
from .routers.users import router as user_router
from .routers.auth import router as auth_router
from .routers.votes import router as vote_router

# Create tables in the database
# models.Base.metadata.create_all(bind=engine) # This line is commented because we are using alembic for migrations for creating tables in the database

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Include routers 
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)

@app.get('/')
async def root():
    return {"message": "Hello World!!"}