import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Tải cấu hình từ file .env
load_dotenv()

# Lấy 3 biến môi trường kết nối Neo4J
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def get_neo4j_driver():
    """ Khởi tạo và trả về driver kết nối với Neo4j """
    if not URI or not USERNAME or not PASSWORD:
        raise ValueError("Thiếu thông tin cấu hình trong file .env. Vui lòng kiểm tra lại.")
        
    try:
        # Khởi tạo driver
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        # Kiểm tra kết nối
        driver.verify_connectivity()
        print("✅ KẾT NỐI ĐẾN NEO4J THÀNH CÔNG!")
        return driver
    except Exception as e:
        print("❌ KẾT NỐI THẤT BẠI.")
        print("Chi tiết lỗi:", e)
        return None

def test_query(driver):
    """ Hàm chạy thử một câu query cơ bản xem DB có dữ liệu hay không """
    if not driver:
        return
    
    # Một lệnh query nhỏ để lấy thử 1 Node trong database ra cấu hình
    query = """
    MATCH (n) 
    RETURN count(n) AS total_nodes
    """
    
    # Chạy lệnh
    try:
        records, summary, keys = driver.execute_query(
            query,
            database_="neo4j",
        )
        for record in records:
            print(f"👉 Số lượng Node hiện có trong Database là: {record['total_nodes']}")
    except Exception as e:
        print("❌ Không thể chạy truy vấn. Lỗi:", e)

if __name__ == "__main__":
    print("Đang tiến hành kết nối Neo4j...")
    neo4j_driver = get_neo4j_driver()
    
    # Nếu kết nối thành công, thử đếm số node hiện có
    if neo4j_driver:
        test_query(neo4j_driver)
        
        # Đóng kết nối sau khi hoàn thành
        neo4j_driver.close()
        print("Đã đóng kết nối an toàn.")
