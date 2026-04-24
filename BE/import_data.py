import os
import pandas as pd
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def create_constraints(driver):
    """
    Tạo các ràng buộc Unique để đảm bảo khi MERGE dữ liệu sẽ cực kỳ nhanh
    (Không có bước này thì import 100k dòng sẽ bị treo).
    """
    print("--- BƯỚC 0: TẠO RÀNG BUỘC (CONSTRAINTS) ---")
    queries = [
        "CREATE CONSTRAINT movie_id IF NOT EXISTS FOR (m:Movie) REQUIRE m.movieId IS UNIQUE",
        "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.userId IS UNIQUE",
        "CREATE CONSTRAINT genre_name IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE"
    ]
    with driver.session() as session:
        for q in queries:
            session.run(q)
    print("Đã tạo constraints xong!")

def clean_csv():
    print("--- BƯỚC 1: ĐỌC VÀ LÀM SẠCH CSV ---")
    # Đường dẫn tuyệt đối tới thư mục tải dataset của bạn
    movies_path = r"D:\khai pha do thi\Neo4J - Gợi ý phim\ml-latest-small\movies.csv"
    ratings_path = r"D:\khai pha do thi\Neo4J - Gợi ý phim\ml-latest-small\ratings.csv"
    
    if not os.path.exists(movies_path) or not os.path.exists(ratings_path):
        print("⚠️ Không tìm thấy file CSV thực tế tại đường dẫn!")
        return None, None
        
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    
    movies_df = movies_df.dropna().drop_duplicates()
    ratings_df = ratings_df.dropna().drop_duplicates()
    
    print(f"Đã đọc xong! Movies: {len(movies_df)} dòng, Ratings: {len(ratings_df)} dòng.")
    return movies_df, ratings_df

def import_to_neo4j(driver, movies_df, ratings_df):
    print("\n--- BƯỚC 2: IMPORT DỮ LIỆU VÀO NEO4J CLOUD ---")
    if movies_df is None or ratings_df is None:
        return
        
    # Import Movies và Thể loại (Genres)
    movie_query = """
    UNWIND $rows AS row
    MERGE (m:Movie {movieId: row.movieId})
    SET m.title = row.title, m.tmdbId = toString(row.movieId), m.plot = "No plot available.", m.released = "Unknown", m.runtime = 120, m.imdbRating = 5.0, m.poster = "https://via.placeholder.com/400x600?text=No+Poster"
    WITH m, row
    UNWIND split(row.genres, '|') AS genre_name
    MERGE (g:Genre {name: genre_name})
    MERGE (m)-[:IN_GENRE]->(g)
    """
    
    # Import Users và Ratings
    rating_query = """
    UNWIND $rows AS row
    MERGE (u:User {userId: row.userId})
    MERGE (m:Movie {movieId: row.movieId})
    MERGE (u)-[r:RATED]->(m)
    SET r.rating = toFloat(row.rating), r.timestamp = row.timestamp
    """
    
    def batch_execute(query, df, batch_size=5000):
        """Hàm chia nhỏ dữ liệu thành các lô (batch) 5000 dòng để không làm quá tải RAM AuraDB"""
        records = df.to_dict('records')
        total = len(records)
        with driver.session() as session:
            for i in range(0, total, batch_size):
                batch = records[i:i+batch_size]
                session.run(query, rows=batch)
                print(f"  Đã import {min(i+batch_size, total)} / {total} dòng...")

    print("Đang đẩy Movies & Genres lên DB...")
    batch_execute(movie_query, movies_df)
    
    print("Đang đẩy Users & Ratings lên DB (Sẽ mất vài phút)...")
    batch_execute(rating_query, ratings_df)
    
    print("🎉 Import thành công toàn bộ dữ liệu!")

if __name__ == "__main__":
    movies_df, ratings_df = clean_csv()
    
    if movies_df is not None:
        # Mở kết nối driver
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        try:
            create_constraints(driver)
            import_to_neo4j(driver, movies_df, ratings_df)
        finally:
            driver.close()
