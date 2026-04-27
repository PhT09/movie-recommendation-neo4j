from models.schemas import Movie
from typing import List
from db.neo4j_conn import neo4j_conn

def recommend_by_user(user_id: int) -> List[Movie]:
    # 1. Thử gợi ý theo user tương tự (Collaborative Filtering)
    query = """
    MATCH (u1:User {userId: $user_id})-[:RATED]->(m:Movie)<-[:RATED]-(u2:User)
    WITH u1, u2, count(m) AS common_movies
    WHERE common_movies >= 10
    MATCH (u2)-[r:RATED]->(rec:Movie)-[:HAS_GENRE]->(g:Genre)
    WHERE toFloat(r.rating) >= 4.0 AND NOT (u1)-[:RATED]->(rec)
    WITH rec, common_movies, max(toFloat(r.rating)) AS max_rating, collect(DISTINCT g.name) AS genres
    RETURN rec.movieId AS id, rec.title AS title, genres, common_movies
    ORDER BY common_movies DESC, max_rating DESC
    LIMIT 10
    """
    records = neo4j_conn.query(query, parameters={"user_id": user_id}, db="neo4j")
    
    # 2. Nếu không có user tương tự, fallback sang gợi ý theo Genre
    if not records:
        query_genre = """
        MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
        WHERE toFloat(r.rating) >= 4.0
        WITH u, g, count(m) AS movies_in_genre
        WHERE movies_in_genre >= 5
        MATCH (rec:Movie)-[:HAS_GENRE]->(g)
        WHERE NOT (u)-[:RATED]->(rec)
        WITH rec, collect(DISTINCT g.name) as genres, sum(movies_in_genre) as score
        RETURN rec.movieId AS id, rec.title AS title, genres
        ORDER BY score DESC
        LIMIT 10
        """
        records = neo4j_conn.query(query_genre, parameters={"user_id": user_id}, db="neo4j")

    # 3. Fallback cho người dùng mới (Cold Start): Gợi ý các phim có độ đánh giá trung bình cao nhất hệ thống
    if not records:
        query_top_rated = """
        MATCH (m:Movie)<-[r:RATED]-()
        WITH m, count(r) AS rating_count, avg(toFloat(r.rating)) AS avg_rating
        WHERE rating_count >= 50
        MATCH (m)-[:HAS_GENRE]->(g:Genre)
        WITH m, avg_rating, rating_count, collect(DISTINCT g.name) AS genres
        RETURN m.movieId AS id, m.title AS title, genres
        ORDER BY avg_rating DESC, rating_count DESC
        LIMIT 10
        """
        records = neo4j_conn.query(query_top_rated, parameters={}, db="neo4j")

    if not records:
        return []

    movies = []
    for r in records:
        try:
            m_id = int(r["id"]) if r["id"] else 0
        except:
            m_id = 0
        movies.append(Movie(id=m_id, title=r["title"], genres=r["genres"]))
    return movies

def recommend_by_movie(movie_id: int) -> List[Movie]:
    # Gợi ý phim tương tự dựa trên thể loại chung
    query = """
    MATCH (m:Movie {movieId: $movie_id})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(rec:Movie)
    WITH rec, count(g) AS common_genres, collect(DISTINCT g.name) AS genres
    RETURN rec.movieId AS id, rec.title AS title, genres
    ORDER BY common_genres DESC
    LIMIT 10
    """
    records = neo4j_conn.query(query, parameters={"movie_id": movie_id}, db="neo4j")
    
    movies = []
    if records:
        for r in records:
            try:
                m_id = int(r["id"]) if r["id"] else 0
            except:
                m_id = 0
            movies.append(Movie(id=m_id, title=r["title"], genres=r["genres"]))
    return movies
