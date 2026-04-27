def get_recommendations_by_genre(driver, user_id, limit):
    """
    Content-based filtering.
    Find movies that share genres with the movies the user has already liked (rated >= 3).
    Exclude movies the user has already seen.
    """
    user_id = int(user_id)
    
    query = """
    MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
    WHERE r.rating >= 3
    WITH u, g
    MATCH (m2:Movie)-[:HAS_GENRE]->(g)
    WHERE NOT (u)-[:RATED]->(m2) AND m2 <> u
    RETURN toInteger(m2.movieId) AS movieId, m2.title AS title, count(g) AS score
    ORDER BY score DESC, m2.title ASC
    LIMIT $limit
    """
    records, _, _ = driver.execute_query(query, userId=user_id, limit=limit)
    return [{"movieId": record["movieId"], "title": record["title"], "score": record["score"]} for record in records]

def get_recommendations_by_user_similarity(driver, user_id, limit):
    """
    Collaborative filtering.
    Find other users who liked the same movies as the current user.
    Recommend movies those similar users liked which the current user hasn't seen yet.
    """
    user_id = int(user_id)
    
    query = """
    MATCH (u:User {userId: $userId})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(other:User)
    WHERE r1.rating >= 3 AND r2.rating >= 3
    WITH u, other, count(m) AS similarity
    ORDER BY similarity DESC
    LIMIT 20
    
    MATCH (other)-[r3:RATED]->(m2:Movie)
    WHERE r3.rating >= 3 AND NOT (u)-[:RATED]->(m2)
    RETURN toInteger(m2.movieId) AS movieId, m2.title AS title, sum(similarity) AS score
    ORDER BY score DESC, m2.title ASC
    LIMIT $limit
    """
    records, _, _ = driver.execute_query(query, userId=user_id, limit=limit)
    return [{"movieId": record["movieId"], "title": record["title"], "score": record["score"]} for record in records]

def get_similar_movies_by_movie(driver, movie_id, limit):
    """
    Find movies similar to a given movie based on shared genres.
    """
    movie_id = int(movie_id)
    query = """
    MATCH (m1:Movie {movieId: $movieId})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(m2:Movie)
    WHERE m1 <> m2
    RETURN toInteger(m2.movieId) AS movieId, m2.title AS title, count(g) AS score
    ORDER BY score DESC, m2.title ASC
    LIMIT $limit
    """
    records, _, _ = driver.execute_query(query, movieId=movie_id, limit=limit)
    return [{"movieId": record["movieId"], "title": record["title"], "score": record["score"]} for record in records]
