import os
import pandas as pd
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Script mẫu cho quá trình ETL: Extract, Transform, Load

def clean_csv():
    """
    Giả lập quá trình đọc và làm sạch dữ liệu từ CSV.
    Ví dụ dùng pandas để loại bỏ dữ liệu rỗng và trùng lặp.
    """
    print("--- BƯỚC 1: LÀM SẠCH CSV ---")
    # Giả sử có file movies.csv và ratings.csv
    movies_path = "data/movies.csv"
    ratings_path = "data/ratings.csv"
    
    if not os.path.exists(movies_path) or not os.path.exists(ratings_path):
        print("⚠️ Không tìm thấy file CSV thực tế. Đây là script mẫu minh hoạ logic làm sạch.")
        print("Logic áp dụng: dropna() để bỏ giá trị NaN, drop_duplicates() để bỏ dòng trùng.")
        return None, None
        
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    
    # Làm sạch dữ liệu
    movies_df = movies_df.dropna().drop_duplicates()
    ratings_df = ratings_df.dropna().drop_duplicates()
    
    print(f"Đã làm sạch! Movies: {len(movies_df)} dòng, Ratings: {len(ratings_df)} dòng.")
    return movies_df, ratings_df

def import_to_neo4j(driver, movies_df, ratings_df):
    """
    Import dữ liệu vào Neo4j bằng Batch Processing (để tối ưu hoá)
    """
    print("\n--- BƯỚC 2: IMPORT DỮ LIỆU VÀO NEO4J ---")
    if movies_df is None or ratings_df is None:
        print("Bỏ qua import vì không có dataframe thực tế (dữ liệu đã có sẵn trên DB).")
        print("Script này minh hoạ việc sử dụng UNWIND trong Cypher để import hàng loạt.")
        return
        
    # Import Movies và Thể loại (Genres)
    movie_query = """
    UNWIND $rows AS row
    MERGE (m:Movie {movieId: row.movieId})
    SET m.title = row.title, m.genres = row.genres
    WITH m, row
    // Giả sử thể loại cách nhau bằng dấu |
    UNWIND split(row.genres, '|') AS genre_name
    MERGE (g:Genre {name: genre_name})
    MERGE (m)-[:HAS_GENRE]->(g)
    """
    
    # Import Users và Ratings
    rating_query = """
    UNWIND $rows AS row
    MERGE (u:User {userId: row.userId})
    MERGE (m:Movie {movieId: row.movieId})
    MERGE (u)-[r:RATED]->(m)
    SET r.rating = toFloat(row.rating), r.timestamp = row.timestamp
    """
    
    # Thực thi (minh hoạ chia thành batch 1000 dòng)
    try:
        # driver.execute_query(movie_query, rows=movies_df.to_dict('records'), database_="neo4j")
        # driver.execute_query(rating_query, rows=ratings_df.to_dict('records'), database_="neo4j")
        print("Import thành công (giả lập)!")
    except Exception as e:
        print("Lỗi import:", e)

if __name__ == "__main__":
    movies_df, ratings_df = clean_csv()
    
    # Mở kết nối driver
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    try:
        import_to_neo4j(driver, movies_df, ratings_df)
    finally:
        driver.close()
