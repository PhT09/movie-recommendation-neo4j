import os
from neo4j import GraphDatabase

URI = "neo4j+ssc://d31317d3.databases.neo4j.io"
USERNAME = "neo4j"

# Các phần có thể nhầm lẫn:
# P1: 02 hoặc O2
# P2: fl hoặc f1
# P3: Iyej hoặc lyej
# P4: 9O hoặc 90

p1s = ["02", "O2"]
p2s = ["fl", "f1"]
p3s = ["Iyej", "lyej"]
p4s = ["9O", "90"]

success = False
for p1 in p1s:
    for p2 in p2s:
        for p3 in p3s:
            for p4 in p4s:
                password = f"DvAx18z50Gpa{p1}{p2}_jfgXrXeUTtL8dti{p3}{p4}UVIMo"
                try:
                    driver = GraphDatabase.driver(URI, auth=(USERNAME, password))
                    driver.verify_connectivity()
                    print(f"✅ TÌM THẤY MẬT KHẨU ĐÚNG: {password}")
                    success = True
                    driver.close()
                    break
                except Exception as e:
                    pass
            if success: break
        if success: break
    if success: break

if not success:
    print("❌ Thử 16 tổ hợp từ hình ảnh đều thất bại. Có thể mật khẩu đã bị đổi trên server.")
