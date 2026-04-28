# Hướng Dẫn Kiểm Thử & Báo Cáo Đồ Án: Hệ Thống Gợi Ý Phim (Neo4j)

Tài liệu này được biên soạn đặc biệt để giúp bạn **Demo trực tiếp** trước hội đồng bảo vệ và **trình bày báo cáo** một cách mượt mà, chuyên nghiệp nhất. Tài liệu kết hợp cả góc nhìn trải nghiệm người dùng (Frontend) và logic truy vấn sâu bên trong (Backend & Database).

---

## PHẦN 1: KỊCH BẢN KIỂM THỬ (TEST CASES) TRỰC TIẾP TRÊN GIAO DIỆN

Để chứng minh hệ thống Gợi ý phim hoạt động thông minh theo cấu trúc **Thác nước (Waterfall)**, hãy thực hiện lần lượt các kịch bản sau ngay trên trình duyệt (`http://localhost:5173/`):

### Kịch bản 1: Lọc Cộng Tác - Collaborative Filtering (Chốt chặn 1)
* **Mục tiêu:** Chứng minh hệ thống có thể phân tích hành vi người dùng, tìm ra những "hảo hữu" có chung khẩu vị và gợi ý phim chéo cho nhau.
* **Thao tác:**
  1. Tại trang Đăng nhập/Khám phá, nhập User ID: **`414`**.
  2. Bấm sang tab **Gợi ý**.
* **Thuyết trình/Báo cáo:**
  - *"Hệ thống nhận diện user 414 là một người dùng lâu năm. Dưới Backend, Neo4j đã chạy thuật toán duyệt đồ thị để tìm ra những người dùng khác có **cùng đánh giá >= 4.0 sao (cùng thích) cho ít nhất 10 bộ phim** với user 414."*
  - *"Từ những 'hảo hữu' này, hệ thống nhặt ra những bộ phim xuất sắc nhất mà họ đã xem (nhưng 414 chưa xem) để hiển thị lên màn hình."*
* **Dấu hiệu nhận biết:** Màn hình trả về các bộ phim kinh điển (Romance, Drama, Comedy) kèm theo điểm đánh giá trung bình `avg_rating` (VD: 4.5 ⭐️) được tính toán Real-time trên góc phải của mỗi thẻ phim.

### Kịch bản 2: Lọc Theo Nội Dung - Content-Based (Chốt chặn 2)
* **Mục tiêu:** Chứng minh hệ thống không bị lỗi nếu người dùng không có ai giống mình (trượt Chốt 1), hệ thống tự động bẻ lái sang Lọc theo Thể loại và **ưu tiên phim có điểm cao nhất**.
* **Thao tác:**
  1. Đăng xuất.
  2. Đăng nhập lại với User ID: **`3`**.
  3. Bấm sang tab **Gợi ý**.
* **Thuyết trình/Báo cáo:**
  - *"User số 3 có rất ít bạn bè chung gu (không có ai cùng thích chung 10 phim). Nếu dùng thuật toán thông thường, màn hình sẽ bị lỗi trắng (Blank). Nhưng hệ thống của em thiết kế cơ chế Fallback."*
  - *"Hệ thống tự động phát hiện User 3 từng đánh giá cao (>= 4.0) cho hơn 5 bộ phim thuộc thể loại Hành động/Kinh dị. Ngay lập tức, thuật toán Content-based được kích hoạt để tìm các phim cùng thể loại này."*
  - *"Điểm đặc biệt là, hệ thống không gợi ý bừa, mà nó sẽ tự động tính toán điểm trung bình của toàn bộ các phim Kinh dị/Hành động, và chỉ đẩy những bộ phim **có điểm trung bình cao nhất (avg_rating DESC)** lên đầu tiên."*
* **Dấu hiệu nhận biết:** Toàn bộ danh sách gợi ý là phim `Action • Thriller • Sci-Fi • Horror` (VD: Resident Evil, Alien), và tất cả đều có điểm rating cực kỳ cao (VD: 5.0 ⭐️).

### Kịch bản 3: Tính năng Smart Search Box (Gợi ý ngay khi tìm kiếm)
* **Mục tiêu:** Trình diễn trải nghiệm người dùng (UX) hiện đại, gợi ý phim ngay từ khi user chưa cần gõ chữ.
* **Thao tác:**
  1. Đăng nhập bằng bất kỳ User ID nào (VD: `414` hoặc `3`).
  2. Tại trang chủ (Khám phá), **Click chuột vào ô Tìm kiếm (Tìm phim...)**.
* **Thuyết trình/Báo cáo:**
  - *"Giống như các nền tảng lớn như Netflix hay Google, khi người dùng vừa click vào thanh tìm kiếm, hệ thống lập tức gọi API Gợi ý để xổ ra một danh sách **✨ Dành riêng cho bạn**."*
  - *"Tính năng này tích hợp sâu thuật toán Gợi ý vào mọi luồng thao tác của người dùng, giúp họ dễ dàng tiếp cận các bộ phim hay nhất mà không cần phải chuyển sang tab Gợi ý."*
* **Dấu hiệu nhận biết:** Một menu thả xuống xuất hiện tuyệt đẹp ngay dưới ô tìm kiếm, chứa top 5 phim hợp gu nhất kèm điểm sao ⭐️.

### Kịch bản 4: Xử Lý Cold Start (Chốt chặn 3 - Cuối cùng)
* **Mục tiêu:** Xử lý triệt để bài toán "Người dùng mới" (Khách vãng lai chưa từng xem phim nào).
* **Thao tác:**
  1. Đăng xuất.
  2. Nhập một ID hoàn toàn mới (VD: **`99999`**).
  3. Bấm sang tab **Gợi ý**.
* **Thuyết trình/Báo cáo:**
  - *"Khi một User mới tinh đăng nhập, đồ thị Neo4j của họ hoàn toàn trống rỗng (không có relationship `[:RATED]`)."*
  - *"Hệ thống chạm đến chốt chặn cuối cùng: Truy vấn toàn bộ Database để tìm ra Top các bộ phim phổ biến nhất (>= 50 lượt đánh giá) và có điểm trung bình cao nhất hệ thống để mời chào người dùng mới."*
* **Dấu hiệu nhận biết:** Màn hình hiển thị các Siêu phẩm vĩ đại nhất mọi thời đại (The Godfather, Shawshank Redemption...).

### Kịch bản 5: Gợi Ý Phim Tương Tự (Item-Based)
* **Mục tiêu:** Khi người dùng tò mò về 1 bộ phim, hệ thống sẽ chèo kéo họ xem các phim có mô-típ tương tự.
* **Thao tác:** Kéo xuống phía dưới của trang Gợi ý (mục "Có thể bạn cũng muốn xem (Theo phim)").
* **Thuyết trình/Báo cáo:** *"Đây là tính năng Item-based. Hệ thống lấy bộ phim đầu tiên và tìm kiếm các phim khác chia sẻ nhiều Node `(:Genre)` chung nhất thông qua relationship `[:HAS_GENRE]`."*

---

## PHẦN 2: BÁO CÁO VỀ SỰ TÍCH HỢP LOGIC (BE & FE)

Để hội đồng đánh giá cao, hãy trình bày cách bạn xử lý Data từ sâu trong DB ra đến màn hình giao diện:

### 1. Sự kết hợp ở Tầng Database (Cypher)
- **Truy vấn Đa Luồng:** Thay vì trả về những dữ liệu thô, các câu lệnh Cypher được viết cực kỳ tối ưu bằng cách dùng lệnh `WITH` và Hàm tập hợp (Aggregations).
- **Tính toán Real-time:** Thay vì lưu cứng `avg_rating` của phim, hệ thống chạy Sub-query ngay lúc truy vấn (`MATCH (rec)<-[all_r:RATED]-() RETURN avg(all_r.rating)`) để luôn đảm bảo điểm trung bình hiển thị ra là mới nhất, làm tròn đến 1 chữ số thập phân.
- **Xử lý trùng lặp (Duplicate Elimination):** Sử dụng hàm `max(common_movies)` để triệt tiêu các bản ghi bị nhân bản khi nhiều user cùng gợi ý 1 bộ phim.

### 2. Sự kết hợp ở Tầng Backend (FastAPI Services)
- **Mô hình Thác Nước (Waterfall Pattern):** Áp dụng cấu trúc `if not movies:` lồng nhau liên tiếp trong `services/recommendation.py`. Backend như một "Nhạc trưởng", nếu truy vấn Neo4j trả về rỗng, nó điều phối gọi ngay truy vấn cấp thấp hơn, đảm bảo API LUÔN trả về HTTP 200 kèm danh sách phim, tuyệt đối không để sập App.
- **Data Mapping (Pydantic):** Chuyển đổi dữ liệu thô của Neo4j thành schema `Movie` chuẩn RESTful, hứng trọn vẹn mảng `genres` và `avg_rating`.

### 3. Sự kết hợp ở Tầng Frontend (React/Vite)
- **Dropdown Suggestion thông minh:** Áp dụng kỹ thuật `onFocus` kết hợp với gọi API Real-time để tạo ra thanh tìm kiếm thông minh tự động gợi ý phim giống hệt mô hình của Netflix/Google.
- **Đồng bộ Logic Người Dùng:** Giao diện hiển thị rõ thông báo *"Đánh giá phim để nhận gợi ý tốt hơn (≥ 4 sao là Thích)"* đồng nhất 100% với điều kiện `>= 4.0` dưới Backend Cypher.
- **Tối ưu UX/UI:** Xử lý hiệu ứng `Skeleton` Loading để user không bị hụt hẫng trong lúc chờ Neo4j duyệt đồ thị phức tạp.

---
**💡 Mẹo khi lên bục bảo vệ:**
Hãy bật sẵn trình duyệt, khi nói đến phần nào, thao tác click chuột trên màn hình theo đúng kịch bản đó. Sự mượt mà của thao tác FE kết hợp cùng lời thuyết minh logic BE sắc bén sẽ giúp bạn ẵm trọn điểm tuyệt đối!
