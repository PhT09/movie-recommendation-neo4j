# Logic Gợi Ý Phim (Movie Recommendation System)

Dự án áp dụng **3 thuật toán chính** kết hợp giữa Lọc cộng tác (Collaborative Filtering), Lọc theo nội dung (Content-based), và Xử lý Cold-Start, được tính toán và xử lý trực tiếp qua Cypher Query trên cơ sở dữ liệu Neo4j. Logic này hiện đang được triển khai chính thức trong file `BE/services/recommendation_service.py`.

---

## 1. Gợi ý phim cho người dùng (User-to-Movie)
Hàm `recommend_by_user(user_id)` hoạt động theo cơ chế **Thác nước (Waterfall/Fallback)** đi tuần tự qua 3 chốt chặn:

### Chốt 1: Lọc cộng tác - Collaborative Filtering (Ưu tiên cao nhất)
- **Mục tiêu:** Tìm ra những bộ phim được đánh giá cao bởi những người dùng có "khẩu vị" cực kỳ giống với User hiện tại.
- **Điều kiện:**
  - Tìm những người dùng khác có **cùng đánh giá >= 4.0 sao** (cùng thích) cho ít nhất **10 bộ phim** với User hiện tại.
  - Phim được gợi ý phải được người dùng tương tự đánh giá từ **4.0 sao trở lên**.
  - Lọc bỏ các bộ phim mà User hiện tại đã xem.
- **Sắp xếp:** Ưu tiên số lượng phim cùng thích (`common_movies DESC`), sau đó ưu tiên theo rating của người dùng tương tự (`rating DESC`).
- **Cypher Code:**
```cypher
MATCH (u1:User {userId: $user_id})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2:User)
WHERE toFloat(r1.rating) >= 4.0 AND toFloat(r2.rating) >= 4.0
WITH u1, u2, count(m) AS common_movies
WHERE common_movies >= 10
MATCH (u2)-[r:RATED]->(rec:Movie)-[:HAS_GENRE]->(g:Genre)
WHERE toFloat(r.rating) >= 4.0 AND NOT (u1)-[:RATED]->(rec)
WITH rec, collect(DISTINCT g.name) AS genres, max(common_movies) AS max_common, max(toFloat(r.rating)) AS max_rating
ORDER BY max_common DESC, max_rating DESC
RETURN rec.movieId AS id, rec.title AS title, genres
LIMIT 10
```

### Chốt 2: Lọc theo nội dung - Content-Based Filtering (Dự phòng 1)
- **Mục tiêu:** Nếu không tìm được ai có chung 10 phim (Chốt 1 thất bại/trả về rỗng), hệ thống sẽ gợi ý phim mới dựa trên các "Thể loại" mà người dùng này yêu thích nhất.
- **Điều kiện:**
  - Tìm ra những Thể loại (Genre) mà User hiện tại đã đánh giá từ **4.0 sao trở lên** cho ít nhất **5 bộ phim**.
  - Gợi ý những phim cùng thể loại đó mà User chưa xem.
- **Sắp xếp:** Ưu tiên những phim có **điểm trung bình cao nhất** (`avg_rating DESC`), sau đó ưu tiên các phim có nhiều Thể loại trùng khớp với sở thích của người dùng nhất (`score DESC`).
- **Cypher Code:**
```cypher
MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
WHERE toFloat(r.rating) >= 4.0
WITH u, g, count(m) AS movies_in_genre
WHERE movies_in_genre >= 5
MATCH (rec:Movie)-[:HAS_GENRE]->(g)
WHERE NOT (u)-[:RATED]->(rec)
WITH rec, collect(DISTINCT g.name) as genres, sum(movies_in_genre) as score
MATCH (rec)<-[all_r:RATED]-()
WITH rec, genres, score, avg(toFloat(all_r.rating)) AS avg_rating
ORDER BY avg_rating DESC, score DESC
RETURN rec.movieId AS id, rec.title AS title, genres
LIMIT 10
```

### Chốt 3: Xử lý Cold-Start - Phim đỉnh nhất (Dự phòng 2)
- **Mục tiêu:** Dành cho người dùng mới tinh chưa từng xem phim, hoặc chưa đáp ứng đủ tiêu chí ở Chốt 2 (chưa có thể loại nào đạt 5 phim >= 4.0 sao). Hệ thống sẽ gợi ý những bộ phim kinh điển, phổ biến và có đánh giá cao nhất trên toàn hệ thống.
- **Điều kiện:**
  - Lấy các phim có từ **50 lượt đánh giá trở lên** (để đảm bảo độ phổ biến và tránh các phim bị "buff" ảo bởi 1 người).
- **Sắp xếp:** Sắp xếp theo điểm đánh giá trung bình cao nhất toàn hệ thống (`avg_rating DESC`) và số lượng người đánh giá (`rating_count DESC`).
- **Cypher Code:**
```cypher
MATCH (m:Movie)<-[r:RATED]-()
WITH m, count(r) AS rating_count, avg(toFloat(r.rating)) AS avg_rating
WHERE rating_count >= 50
MATCH (m)-[:HAS_GENRE]->(g:Genre)
WITH m, avg_rating, rating_count, collect(DISTINCT g.name) AS genres
RETURN m.movieId AS id, m.title AS title, genres
ORDER BY avg_rating DESC, rating_count DESC
LIMIT 10
```

---

## 2. Gợi ý phim tương tự (Movie-to-Movie)
Hàm `recommend_by_movie(movie_id)` hoạt động độc lập và được sử dụng khi User đang mở xem trang Chi tiết của một bộ phim bất kỳ.

### Thuật toán: Item-Based (Dựa trên Thể loại)
- **Mục tiêu:** Gợi ý các phim khác có đặc điểm Thể loại giống hệt với phim hiện tại.
- **Điều kiện:** Tìm các bộ phim khác chia sẻ cùng Thể loại (`HAS_GENRE`) với bộ phim đang xem.
- **Sắp xếp:** Bộ phim nào chia sẻ càng nhiều Thể loại chung với phim hiện tại (ví dụ: trùng cả Action, Sci-Fi và Thriller) thì sẽ xếp vị trí càng cao (`common_genres DESC`).
- **Cypher Code:**
```cypher
MATCH (m:Movie {movieId: $movie_id})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(rec:Movie)
WITH rec, count(g) AS common_genres, collect(DISTINCT g.name) AS genres
RETURN rec.movieId AS id, rec.title AS title, genres
ORDER BY common_genres DESC
LIMIT 10
```

*(Lưu ý: Mọi logic thử nghiệm cũ trong `BE/database/recommendation.py` hiện đã được loại bỏ, và Backend API hiện tại 100% sử dụng toàn bộ luồng logic 3 chốt này).*
