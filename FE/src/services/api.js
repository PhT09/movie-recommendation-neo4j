import axios from 'axios';

// ==========================================
// CONFIGURATION
// ==========================================
// Đặt USE_MOCK = true khi Backend chưa sẵn sàng
const USE_MOCK = true; 
const API_BASE_URL = 'http://localhost:8000/api'; // Thay đổi theo URL backend FastAPI của bạn

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==========================================
// MOCK DATA
// ==========================================
const MOCK_MOVIES = [
  { id: '1', title: 'The Matrix', genres: ['Action', 'Sci-Fi'], year: 1999 },
  { id: '2', title: 'Inception', genres: ['Action', 'Sci-Fi', 'Thriller'], year: 2010 },
  { id: '3', title: 'Toy Story', genres: ['Animation', 'Comedy'], year: 1995 },
  { id: '4', title: 'The Dark Knight', genres: ['Action', 'Crime'], year: 2008 },
  { id: '5', title: 'Interstellar', genres: ['Adventure', 'Drama', 'Sci-Fi'], year: 2014 },
];

const MOCK_RECOMMENDATIONS_USER = [
  { 
    id: '4', 
    title: 'The Dark Knight', 
    genres: ['Action', 'Crime'], 
    year: 2008, 
    reason: 'Vì bạn đã thích thể loại Action'
  },
  { 
    id: '2', 
    title: 'Inception', 
    genres: ['Action', 'Sci-Fi', 'Thriller'], 
    year: 2010, 
    reason: 'Những người dùng tương tự cũng thích'
  }
];

// Helper để delay mock response tạo cảm giác như gọi API thật
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// ==========================================
// API SERVICES
// ==========================================
export const ApiService = {
  // Lấy danh sách phim để người dùng đánh giá
  getMovies: async (search = '', genre = '') => {
    if (USE_MOCK) {
      await delay(500);
      return MOCK_MOVIES.filter(m => 
        m.title.toLowerCase().includes(search.toLowerCase()) &&
        (genre ? m.genres.includes(genre) : true)
      );
    }
    const response = await axiosInstance.get('/movies', { params: { search, genre } });
    return response.data;
  },

  // ------------------------------------------
  // RATING CRUD (1-5 stars, Backend: >=3 is LIKE)
  // ------------------------------------------
  createRating: async (userId, movieId, rating) => {
    if (USE_MOCK) {
      await delay(300);
      console.log(`[MOCK] POST /rating: User ${userId} rated Movie ${movieId} with ${rating} stars`);
      return { success: true, message: 'Đã lưu đánh giá' };
    }
    const response = await axiosInstance.post('/rating', { userId, movieId, rating });
    return response.data;
  },

  updateRating: async (userId, movieId, rating) => {
    if (USE_MOCK) {
      await delay(300);
      console.log(`[MOCK] PUT /rating: User ${userId} updated Movie ${movieId} rating to ${rating} stars`);
      return { success: true, message: 'Đã cập nhật đánh giá' };
    }
    const response = await axiosInstance.put('/rating', { userId, movieId, rating });
    return response.data;
  },

  deleteRating: async (userId, movieId) => {
    if (USE_MOCK) {
      await delay(300);
      console.log(`[MOCK] DELETE /rating: User ${userId} deleted rating for Movie ${movieId}`);
      return { success: true, message: 'Đã xóa đánh giá' };
    }
    const response = await axiosInstance.delete('/rating', { data: { userId, movieId } });
    return response.data;
  },

  // ------------------------------------------
  // RECOMMENDATIONS
  // ------------------------------------------
  // Gợi ý theo User
  getRecommendByUser: async (userId) => {
    if (USE_MOCK) {
      await delay(800);
      console.log(`[MOCK] GET /recommend/user/${userId}`);
      return MOCK_RECOMMENDATIONS_USER;
    }
    const response = await axiosInstance.get(`/recommend/user/${userId}`);
    return response.data;
  },

  // Gợi ý theo một bộ phim cụ thể
  getRecommendByMovie: async (movieId) => {
    if (USE_MOCK) {
      await delay(800);
      console.log(`[MOCK] GET /recommend/movie/${movieId}`);
      return MOCK_MOVIES.filter(m => m.id !== movieId).slice(0, 3).map(m => ({
        ...m,
        reason: 'Khá giống với phim bạn đang xem'
      }));
    }
    const response = await axiosInstance.get(`/recommend/movie/${movieId}`);
    return response.data;
  }
};
