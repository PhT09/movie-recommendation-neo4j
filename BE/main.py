from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import recommendation, rating, movie, user
from database.connection import neo4j_conn

app = FastAPI(
    title="Movie Recommendation API",
    description="Backend API layer for Movie Recommendation System (Member C)",
    version="1.0.0"
)

# CORS middleware to allow FE to call BE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommendation.router)
app.include_router(rating.router)
app.include_router(movie.router)
app.include_router(user.router)

@app.on_event("shutdown")
def shutdown_event():
    neo4j_conn.close()

@app.get("/")
def root():
    return {"message": "Welcome to Movie Recommendation API!"}

# Trigger uvicorn reload
