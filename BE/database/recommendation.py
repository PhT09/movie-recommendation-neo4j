def get_recommendations_by_user_similarity(driver, user_id, limit):
    user_id = int(user_id)
    query = """
    MATCH (u1:User {userId: $userId})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2:User)
    WHERE toFloat(r1.rating) >= 4.0 AND toFloat(r2.rating) >= 4.0
    WITH u1, u2, count(m) AS common_movies
    WHERE common_movies >= 10
    MATCH (u2)-[r:RATED]->(rec:Movie)-[:HAS_GENRE]->(g:Genre)
    WHERE toFloat(r.rating) >= 4.0 AND NOT (u1)-[:RATED]->(rec)
    WITH rec, collect(DISTINCT g.name) AS genres, max(common_movies) AS max_common, max(toFloat(r.rating)) AS max_rating
    ORDER BY max_common DESC, max_rating DESC
    LIMIT $limit
    MATCH (rec)<-[all_r:RATED]-()
    RETURN rec.movieId AS movieId, rec.title AS title, genres, round(avg(toFloat(all_r.rating))*10)/10.0 AS avg_rating
    """
    records, _, _ = driver.execute_query(query, userId=user_id, limit=limit, database_="neo4j")
    return [{"movieId": r["movieId"], "title": r["title"], "genres": r["genres"], "avg_rating": r["avg_rating"]} for r in records]

def get_recommendations_by_genre(driver, user_id, limit):
    user_id = int(user_id)
    query = """
    MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
    WHERE toFloat(r.rating) >= 4.0
    WITH u, g, count(m) AS movies_in_genre
    WHERE movies_in_genre >= 5
    MATCH (rec:Movie)-[:HAS_GENRE]->(g)
    WHERE NOT (u)-[:RATED]->(rec)
    WITH rec, collect(DISTINCT g.name) as genres, sum(movies_in_genre) as score
    MATCH (rec)<-[all_r:RATED]-()
    WITH rec, genres, score, avg(toFloat(all_r.rating)) AS avg_rating
    ORDER BY avg_rating DESC, score DESC
    LIMIT $limit
    RETURN rec.movieId AS movieId, rec.title AS title, genres, round(avg_rating*10)/10.0 AS avg_rating
    """
    records, _, _ = driver.execute_query(query, userId=user_id, limit=limit, database_="neo4j")
    return [{"movieId": r["movieId"], "title": r["title"], "genres": r["genres"], "avg_rating": r["avg_rating"]} for r in records]

def get_top_rated_movies(driver, limit):
    query = """
    MATCH (m:Movie)<-[r:RATED]-()
    WITH m, count(r) AS rating_count, avg(toFloat(r.rating)) AS avg_rating
    WHERE rating_count >= 50
    MATCH (m)-[:HAS_GENRE]->(g:Genre)
    WITH m, avg_rating, rating_count, collect(DISTINCT g.name) AS genres
    ORDER BY avg_rating DESC, rating_count DESC
    LIMIT $limit
    RETURN m.movieId AS movieId, m.title AS title, genres, round(avg_rating*10)/10.0 AS avg_rating
    """
    records, _, _ = driver.execute_query(query, limit=limit, database_="neo4j")
    return [{"movieId": r["movieId"], "title": r["title"], "genres": r["genres"], "avg_rating": r["avg_rating"]} for r in records]

def get_similar_movies_by_movie(driver, movie_id, limit):
    movie_id = int(movie_id)
    query = """
    MATCH (m:Movie {movieId: $movieId})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(rec:Movie)
    WITH rec, count(g) AS common_genres, collect(DISTINCT g.name) AS genres
    ORDER BY common_genres DESC
    LIMIT $limit
    MATCH (rec)<-[all_r:RATED]-()
    RETURN rec.movieId AS movieId, rec.title AS title, genres, round(avg(toFloat(all_r.rating))*10)/10.0 AS avg_rating
    """
    records, _, _ = driver.execute_query(query, movieId=movie_id, limit=limit, database_="neo4j")
    return [{"movieId": r["movieId"], "title": r["title"], "genres": r["genres"], "avg_rating": r["avg_rating"]} for r in records]
