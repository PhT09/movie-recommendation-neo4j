import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def get_test_users(driver):
    # Find a user who has rated many movies
    query = """
    MATCH (u:User)-[:RATED]->(m:Movie)
    RETURN u.userId AS userId, count(m) AS count
    ORDER BY count DESC LIMIT 5
    """
    records, _, _ = driver.execute_query(query, database_="neo4j")
    print("Users with most ratings:")
    for r in records:
        print(f"User {r['userId']} - {r['count']} ratings")
    return records[0]['userId'] if records else None

def recommend_by_genre(driver, user_id):
    """
    Theo genre (content-based đơn giản, thích 5 phim cùng 1 thể loại thì thích thể loại đó)
    Giả sử "thích" là rating >= 4.0
    """
    query = """
    MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
    WHERE toFloat(r.rating) >= 4.0
    WITH u, g, count(m) AS movies_in_genre
    WHERE movies_in_genre >= 5
    
    // Tìm các phim thuộc thể loại đó mà user chưa xem
    MATCH (g)<-[:HAS_GENRE]-(rec:Movie)
    WHERE NOT (u)-[:RATED]->(rec)
    
    RETURN rec.title AS recommended_movie, g.name AS genre, movies_in_genre
    LIMIT 10
    """
    print(f"\n--- GỢI Ý THEO GENRE CHO USER {user_id} ---")
    records, _, _ = driver.execute_query(query, user_id=user_id, database_="neo4j")
    if not records:
        print("Không có gợi ý nào.")
    for r in records:
        print(f"Phim: {r['recommended_movie']} | Thể loại: {r['genre']} (Đã thích {r['movies_in_genre']} phim)")

def recommend_by_similar_users(driver, user_id):
    """
    Theo user tương tự (≥ 500 phim giống nhau)
    """
    query = """
    MATCH (u1:User {userId: $user_id})-[:RATED]->(m:Movie)<-[:RATED]-(u2:User)
    WITH u1, u2, count(m) AS common_movies
    // Lọc user có >= 500 phim giống nhau
    WHERE common_movies >= 500
    
    // Tìm phim u2 đã xem (và thích, rating >= 4.0) mà u1 chưa xem
    MATCH (u2)-[r:RATED]->(rec:Movie)
    WHERE toFloat(r.rating) >= 4.0 AND NOT (u1)-[:RATED]->(rec)
    
    RETURN rec.title AS recommended_movie, u2.userId AS similar_user, common_movies
    LIMIT 10
    """
    print(f"\n--- GỢI Ý THEO USER TƯƠNG TỰ (>= 500 PHIM CHUNG) CHO USER {user_id} ---")
    records, _, _ = driver.execute_query(query, user_id=user_id, database_="neo4j")
    if not records:
        print("Không tìm thấy user nào có >= 500 phim chung, hoặc không có phim gợi ý.")
    for r in records:
        print(f"Phim: {r['recommended_movie']} | User tương tự: {r['similar_user']} ({r['common_movies']} phim chung)")

if __name__ == "__main__":
    print("Đang kết nối Neo4j...")
    try:
        user_id = get_test_users(driver)
        if user_id:
            recommend_by_genre(driver, user_id)
            recommend_by_similar_users(driver, user_id)
    finally:
        driver.close()
