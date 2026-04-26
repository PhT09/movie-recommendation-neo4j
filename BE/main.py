from fastapi import FastAPI
from routers import recommendation, rating
from db.neo4j_conn import neo4j_conn

app = FastAPI(
    title="Movie Recommendation API",
    description="Backend API layer for Movie Recommendation System (Member C)",
    version="1.0.0"
)

app.include_router(recommendation.router)
app.include_router(rating.router)

@app.on_event("shutdown")
def shutdown_event():
    neo4j_conn.close()

@app.get("/")
def root():
    return {"message": "Welcome to Movie Recommendation API!"}
