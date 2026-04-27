# Các Câu Lệnh Cypher

File này dùng để lưu trữ các câu lệnh Cypher thường dùng để mọi người trong nhóm có thể dễ dàng copy và test trên giao diện Neo4j Workspace.

## 1. Kiểm tra tổng số Node và Relationship hiện có
```cypher
MATCH (n) RETURN count(n) AS TotalNodes;
MATCH ()-[r]->() RETURN count(r) AS TotalRelationships;
```

## 2. Lấy ra một số User mẫu
```cypher
MATCH (u:User) 
RETURN u 
LIMIT 10;
```

## 3. Lấy ra một số Phim (Movie) mẫu
```cypher
MATCH (m:Movie) 
RETURN m 
LIMIT 10;
```

## 4. Xem mối quan hệ Đánh Giá (User RATED Movie)
*Lệnh này sẽ hiển thị mũi tên nối giữa người dùng và phim, xem rõ số sao (rating).*
```cypher
MATCH (u:User)-[r:RATED]->(m:Movie) 
RETURN u, r, m 
LIMIT 15;
```

## 5. Xóa toàn bộ dữ liệu (CẢNH BÁO: RẤT NGUY HIỂM)
*Chỉ dùng khi muốn reset lại toàn bộ Database.*
```cypher
MATCH (n) DETACH DELETE n;
```
