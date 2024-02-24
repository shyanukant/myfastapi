from fastapi import FastAPI
from .database import engine
from . import models
from .routers.posts import router as post_router
from .routers.users import router as user_router
from .routers.auth import router as auth_router
from .routers.votes import router as vote_router

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers 
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)

@app.get('/')
async def root():
    return {"message": "Hello World!!"}