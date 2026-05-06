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

def register_user(driver, name):
    """
    Find the max userId and create a new one.
    """
    query_max_id = "MATCH (u:User) RETURN MAX(u.userId) AS maxUserId"
    records, _, _ = driver.execute_query(query_max_id)
    max_user_id = records[0]["maxUserId"] if records and records[0]["maxUserId"] is not None else 0
    new_id = max_user_id + 1
    
    query_create = """
    CREATE (u:User {userId: $new_id, name: $name})
    RETURN u.userId AS userId, u.name AS name
    """
    records, _, _ = driver.execute_query(query_create, new_id=new_id, name=name)
    return records[0] if records else None

def get_user_by_id(driver, user_id):
    """
    Find user by userId.
    """
    query = "MATCH (u:User {userId: $user_id}) RETURN u.userId AS userId, u.name AS name LIMIT 1"
    records, _, _ = driver.execute_query(query, user_id=int(user_id))
    return records[0] if records else None

def search_movies(driver, search_term=None, genre=None, skip=0, limit=50):
    """
    Search movies by title and/or genre.
    """
    query = "MATCH (m:Movie) WHERE 1=1"
    params = {}
    
    if search_term:
        query += " AND toLower(m.title) CONTAINS toLower($search)"
        params["search"] = search_term
        
    if genre:
        query += " AND (m)-[:HAS_GENRE]->(:Genre {name: $genre})"
        params["genre"] = genre
        
    query += " RETURN toInteger(m.movieId) AS movieId, m.title AS title SKIP $skip LIMIT $limit"
    params["skip"] = skip
    params["limit"] = limit
    
    records, _, _ = driver.execute_query(query, **params)
    return [{"movieId": record["movieId"], "title": record["title"]} for record in records]

def get_user_ratings(driver, user_id):
    """
    Get all ratings for a user.
    """
    query = """
    MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie)
    RETURN u.userId AS userId, m.movieId AS movieId, r.rating AS rating, r.timestamp AS timestamp
    """
    records, _, _ = driver.execute_query(query, userId=int(user_id))
    return [{"userId": record["userId"], "movieId": record["movieId"], "rating": record["rating"], "timestamp": record["timestamp"]} for record in records]
