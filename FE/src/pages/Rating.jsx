import React, { useState, useEffect, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { ApiService } from '../services/api';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Rating as PrimeRating } from 'primereact/rating';
import { Toast } from 'primereact/toast';
import { useRef } from 'react';

export default function Rating() {
  const { userId } = useContext(UserContext);
  const [movies, setMovies] = useState([]);
  const [search, setSearch] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const [loading, setLoading] = useState(false);
  const [userRatings, setUserRatings] = useState({});
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const toast = useRef(null);

  const [genresOptions, setGenresOptions] = useState([{ label: 'Tất cả', value: '' }]);
  const [skip, setSkip] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const LIMIT = 50;

  useEffect(() => {
    const fetchGenres = async () => {
      try {
        const data = await ApiService.getGenres();
        const formattedGenres = data.map(g => ({ label: g, value: g }));
        setGenresOptions([{ label: 'Tất cả', value: '' }, ...formattedGenres]);
      } catch (err) {
        console.error("Lỗi khi tải thể loại phim", err);
      }
    };
    fetchGenres();
  }, []);

  const fetchMovies = async (reset = false) => {
    if (reset) {
      setLoading(true);
    }
    try {
      const currentSkip = reset ? 0 : skip;
      let data = [];
      
      if (!search && !selectedGenre && currentSkip === 0 && userId) {
        // Lấy gợi ý phim cho User trước
        const recs = await ApiService.getRecommendByUser(userId);
        // Lấy thêm phim ngẫu nhiên để lấp đầy phần còn lại
        const randoms = await ApiService.getMovies(search, selectedGenre, 0, LIMIT - recs.length);
        
        // Loại bỏ phim trùng lặp
        const recIds = new Set(recs.map(r => r.id));
        const filteredRandoms = randoms.filter(r => !recIds.has(r.id));
        
        data = [...recs, ...filteredRandoms];
      } else {
        data = await ApiService.getMovies(search, selectedGenre, currentSkip, LIMIT);
      }
      
      if (reset) {
        setMovies(data);
        setSkip(LIMIT);
      } else {
        setMovies(prev => [...prev, ...data]);
        setSkip(currentSkip + LIMIT);
      }
      
      if (data.length < LIMIT) {
        setHasMore(false);
      } else {
        setHasMore(true);
      }
    } catch (error) {
      toast.current.show({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách phim' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovies(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search, selectedGenre]);

  useEffect(() => {
    const fetchRatings = async () => {
      if (userId) {
        try {
          const ratings = await ApiService.getUserRatings(userId);
          const ratingMap = {};
          ratings.forEach(r => {
            ratingMap[r.movieId] = r.rating;
          });
          setUserRatings(ratingMap);
        } catch (error) {
          console.error("Không thể tải lịch sử đánh giá", error);
        }
      }
    };
    fetchRatings();
  }, [userId]);

  const handleRatingChange = async (e, movieId) => {
    const newRating = e.value;
    const oldRating = userRatings[movieId];

    // Update local state optimistic
    setUserRatings(prev => ({ ...prev, [movieId]: newRating }));

    try {
      if (newRating === null || newRating === 0) {
        // user clicked the cancel icon => DELETE
        if (oldRating) {
          await ApiService.deleteRating(userId, movieId);
          toast.current.show({ severity: 'info', summary: 'Đã xóa', detail: 'Đã xóa đánh giá', life: 2000 });
        }
      } else {
        if (oldRating) {
          // Update
          await ApiService.updateRating(userId, movieId, newRating);
          toast.current.show({ severity: 'success', summary: 'Cập nhật', detail: `Đã cập nhật ${newRating} sao`, life: 2000 });
        } else {
          // Create
          await ApiService.createRating(userId, movieId, newRating);
          toast.current.show({ severity: 'success', summary: 'Đánh giá', detail: `Đã đánh giá ${newRating} sao`, life: 2000 });
        }
      }
    } catch (err) {
      // rollback on error
      setUserRatings(prev => ({ ...prev, [movieId]: oldRating }));
      toast.current.show({ severity: 'error', summary: 'Lỗi', detail: 'Không thể lưu đánh giá', life: 3000 });
    }
  };

  const handleSearchFocus = async () => {
    setShowSuggestions(true);
    if (userId && suggestions.length === 0) {
      try {
        const data = await ApiService.getRecommendByUser(userId);
        setSuggestions(data.slice(0, 5)); // Limit to top 5 for dropdown
      } catch (err) {
        console.error("Lỗi khi tải gợi ý", err);
      }
    }
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <Toast ref={toast} />

      <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Khám phá & Đánh giá</h2>
          <p className="text-slate-400">Đánh giá phim để nhận gợi ý tốt hơn (≥ 4 sao là Thích)</p>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
          <div className="relative w-full sm:w-64 flex flex-col">
            <div className="relative w-full flex">
              <i className="pi pi-search text-slate-400 absolute left-4 top-1/2 -translate-y-1/2 z-10" />
              <InputText
                placeholder="Tìm phim..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onFocus={handleSearchFocus}
                onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl py-[0.85rem] pr-3 focus:ring-2 focus:ring-indigo-500 outline-none font-sans shadow-sm"
                style={{ paddingLeft: '2.75rem' }}
              />
            </div>
            {showSuggestions && suggestions.length > 0 && (
              <div className="absolute top-[110%] left-0 w-full bg-slate-800 border border-slate-700 rounded-xl shadow-2xl z-50 max-h-64 overflow-y-auto">
                <div className="px-3 py-2 text-xs text-slate-400 uppercase font-bold border-b border-slate-700 bg-slate-900/50 flex items-center gap-2">
                  <i className="pi pi-sparkles text-amber-400"></i> Dành riêng cho bạn
                </div>
                {suggestions.map(movie => (
                  <div key={movie.id} 
                       className="px-4 py-3 hover:bg-slate-700 cursor-pointer text-white flex justify-between items-center transition-colors border-b border-slate-700/50 last:border-0"
                       onClick={() => setSearch(movie.title)}>
                    <div className="line-clamp-1 flex-1 text-sm font-medium pr-2">{movie.title}</div>
                    {movie.avg_rating && <div className="text-yellow-500 text-xs flex items-center gap-1 font-bold whitespace-nowrap"><i className="pi pi-star-fill text-[10px]"></i>{movie.avg_rating}</div>}
                  </div>
                ))}
              </div>
            )}
          </div>
          <Dropdown
            value={selectedGenre}
            options={genresOptions}
            onChange={(e) => setSelectedGenre(e.value)}
            placeholder="Thể loại"
            className="w-full sm:w-48 bg-slate-800 border border-slate-700 text-white rounded-xl shadow-sm flex items-center"
            panelClassName="bg-slate-800 text-white border-slate-700"
            pt={{ input: { className: 'py-[0.85rem]' } }}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 lg:grid-cols-5 gap-6">
        {movies.map(movie => (
          <div key={movie.id} className="bg-slate-800 rounded-2xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 hover:-translate-y-1 group flex flex-col min-h-[220px]">
            <div className="p-5 flex flex-col flex-grow items-center justify-center text-center relative border-b border-slate-700/30 bg-slate-800/50">
              <h3 className="font-bold text-xl text-white mt-4 mb-2 line-clamp-2" title={movie.title}>{movie.title}</h3>
              <p className="text-xs text-slate-400">{movie.genres ? movie.genres.join(' • ') : 'Không rõ thể loại'}</p>
            </div>
            <div className="p-4 mt-auto">
              <div className="flex justify-center py-2 bg-slate-900/50 rounded-xl">
                <PrimeRating
                  value={userRatings[movie.id] || 0}
                  onChange={(e) => handleRatingChange(e, movie.id)}
                  cancel={false}
                  className="text-amber-400 gap-1"
                  pt={{
                    onIcon: { className: 'text-amber-400' },
                    offIcon: { className: 'text-slate-600' }
                  }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      {loading && (
        <div className="flex justify-center p-8">
          <i className="pi pi-spin pi-spinner text-3xl text-indigo-500"></i>
        </div>
      )}

      {!loading && hasMore && movies.length > 0 && (
        <div className="flex justify-center mt-8">
          <button 
            onClick={() => fetchMovies(false)}
            className="px-6 py-2.5 bg-slate-800 hover:bg-indigo-600 text-white rounded-full font-medium transition-colors border border-slate-700 hover:border-indigo-500 shadow-md flex items-center gap-2"
          >
            <i className="pi pi-refresh"></i> Tải thêm phim
          </button>
        </div>
      )}

      {!loading && movies.length === 0 && (
        <div className="text-center py-16 text-slate-400">
          <i className="pi pi-inbox text-5xl mb-4 opacity-50"></i>
          <p>Không tìm thấy phim nào phù hợp.</p>
        </div>
      )}
    </div>
  );
}
