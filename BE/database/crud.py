def fetch_movies(driver, limit, skip):
    """
    Retrieve a list of movies from the database.
    Uses SKIP and LIMIT for pagination.
    Returns a list of dictionaries containing movieId and title.
    """
    query = """
    MATCH (m:Movie)
    RETURN toInteger(m.movieId) AS movieId, m.title AS title
    SKIP $skip LIMIT $limit
    """
    records, _, _ = driver.execute_query(query, skip=skip, limit=limit)
    return [{"movieId": record["movieId"], "title": record["title"]} for record in records]

def sync_rating_edge(driver, user_id, movie_id, rating):
    """
    Implement the business logic for ratings:
    - If rating >= 3: Use MERGE to create or update the [:RATED] relationship between the User and the Movie, setting the rating property.
    - If rating < 3: MATCH and DELETE the existing [:RATED] relationship if it exists.
    """
    user_id = int(user_id)
    movie_id = int(movie_id)
    
    if rating >= 3:
        query = """
        MERGE (u:User {userId: $userId})
        MERGE (m:Movie {movieId: $movieId})
        MERGE (u)-[r:RATED]->(m)
        SET r.rating = $rating
        """
        driver.execute_query(query, userId=user_id, movieId=movie_id, rating=rating)
    else:
        query = """
        MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie {movieId: $movieId})
        DELETE r
        """
        driver.execute_query(query, userId=user_id, movieId=movie_id)

def fetch_genres(driver):
    """
    Retrieve a list of all genres from the database.
    Returns a list of genre names.
    """
    query = """
    MATCH (g:Genre)
    RETURN g.name AS name
    ORDER BY name ASC
    """
    records, _, _ = driver.execute_query(query)
    return [record["name"] for record in records]
