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
  const toast = useRef(null);

  const genres = [
    { label: 'Tất cả', value: '' },
    { label: 'Action', value: 'Action' },
    { label: 'Sci-Fi', value: 'Sci-Fi' },
    { label: 'Comedy', value: 'Comedy' },
    { label: 'Drama', value: 'Drama' },
  ];

  const fetchMovies = async () => {
    setLoading(true);
    try {
      const data = await ApiService.getMovies(search, selectedGenre);
      setMovies(data);
    } catch (error) {
      toast.current.show({ severity: 'error', summary: 'Lỗi', detail: 'Không thể tải danh sách phim' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovies();
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

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <Toast ref={toast} />

      <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Khám phá & Đánh giá</h2>
          <p className="text-slate-400">Đánh giá phim để nhận gợi ý tốt hơn (≥ 3 sao là Thích)</p>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
          <div className="relative w-full sm:w-64 flex">
            <i className="pi pi-search text-slate-400 absolute left-4 top-1/2 -translate-y-1/2 z-10" />
            <InputText
              placeholder="Tìm phim..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl py-[0.85rem] pr-3 focus:ring-2 focus:ring-indigo-500 outline-none font-sans shadow-sm"
              style={{ paddingLeft: '2.75rem' }}
            />
          </div>
          <Dropdown
            value={selectedGenre}
            options={genres}
            onChange={(e) => setSelectedGenre(e.value)}
            placeholder="Thể loại"
            className="w-full sm:w-48 bg-slate-800 border border-slate-700 text-white rounded-xl shadow-sm flex items-center"
            panelClassName="bg-slate-800 text-white border-slate-700"
            pt={{ input: { className: 'py-[0.85rem]' } }}
          />
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center p-12">
          <i className="pi pi-spin pi-spinner text-4xl text-indigo-500"></i>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 lg:grid-cols-5 gap-6">
          {movies.map(movie => (
            <div key={movie.id} className="bg-slate-800 rounded-2xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 hover:-translate-y-1 group flex flex-col min-h-[220px]">
              <div className="p-5 flex flex-col flex-grow items-center justify-center text-center relative border-b border-slate-700/30 bg-slate-800/50">
                <div className="absolute top-3 right-3">
                  <span className="text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 py-1 rounded-md shadow-sm">
                    {movie.year || 'N/A'}
                  </span>
                </div>
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
