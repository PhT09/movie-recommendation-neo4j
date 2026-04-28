import React, { useState, useEffect, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { ApiService } from '../services/api';
import { Carousel } from 'primereact/carousel';
import { Tag } from 'primereact/tag';
import { Button } from 'primereact/button';
import { Skeleton } from 'primereact/skeleton';

export default function Recommendation() {
  const { userId } = useContext(UserContext);
  const [userRecs, setUserRecs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecs = async () => {
      setLoading(true);
      try {
        const data = await ApiService.getRecommendByUser(userId);
        setUserRecs(data);
      } catch (err) {
        console.error("Error fetching recommendations", err);
      } finally {
        setLoading(false);
      }
    };
    if (userId) {
      fetchRecs();
    }
  }, [userId]);

  const responsiveOptions = [
    { breakpoint: '1199px', numVisible: 3, numScroll: 1 },
    { breakpoint: '991px', numVisible: 2, numScroll: 1 },
    { breakpoint: '767px', numVisible: 1, numScroll: 1 }
  ];

  const movieTemplate = (movie) => {
    return (
      <div className="bg-slate-800 border border-slate-700/50 rounded-2xl mx-3 p-4 flex flex-col h-full shadow-lg hover:shadow-indigo-500/20 transition-all duration-300 group min-h-[280px]">
        <div className="flex flex-col items-center justify-center text-center p-6 bg-slate-800/50 border-b border-slate-700/30 rounded-t-xl mb-4 relative flex-grow">
          {movie.avg_rating && (
            <div className="absolute top-2 right-2 bg-yellow-500/20 text-yellow-500 text-xs font-bold px-2 py-1 rounded flex items-center gap-1">
              <i className="pi pi-star-fill text-xs"></i> {movie.avg_rating}
            </div>
          )}
          <h3 className="text-2xl font-bold text-white mb-2 line-clamp-2 mt-4">{movie.title}</h3>
          <p className="text-sm text-slate-400">{movie.genres ? movie.genres.join(' • ') : 'Không rõ thể loại'}</p>
        </div>
      </div>
    );
  };

  const skeletonTemplate = () => {
    return (
      <div className="bg-slate-800 border border-slate-700/50 rounded-2xl mx-3 p-4 flex flex-col h-full min-h-[280px]">
        <div className="flex flex-col items-center justify-center p-6 bg-slate-800/50 border-b border-slate-700/30 rounded-t-xl mb-4 flex-grow">
          <Skeleton width="60%" height="2rem" className="mb-4 bg-slate-700"></Skeleton>
          <Skeleton width="40%" height="1rem" className="bg-slate-700"></Skeleton>
        </div>
        <Skeleton width="100%" height="4rem" className="mt-auto bg-slate-700 rounded-xl"></Skeleton>
      </div>
    );
  };

  if (!userId) {
    return (
      <div className="text-center py-20 text-slate-400">
        Vui lòng đăng nhập để xem gợi ý.
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <div className="flex items-center gap-3 mb-8">
        <div className="h-10 w-10 bg-indigo-500/20 rounded-lg flex items-center justify-center text-indigo-400">
          <i className="pi pi-compass text-xl"></i>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-white leading-tight">Dành riêng cho bạn</h2>
          <p className="text-slate-400 text-sm">Dựa trên sở thích và đánh giá của bạn</p>
        </div>
      </div>

      {loading ? (
        <Carousel 
          value={[1,2,3,4]} 
          numVisible={3} 
          numScroll={1} 
          responsiveOptions={responsiveOptions} 
          itemTemplate={skeletonTemplate} 
          circular 
          showNavigators={false} 
          showIndicators={false}
        />
      ) : userRecs.length > 0 ? (
        <Carousel 
          value={userRecs} 
          numVisible={3} 
          numScroll={1} 
          responsiveOptions={responsiveOptions} 
          itemTemplate={movieTemplate} 
          circular
          autoplayInterval={4000}
        />
      ) : (
        <div className="text-center py-16 bg-slate-800/50 border border-slate-700/50 rounded-2xl">
          <i className="pi pi-info-circle text-4xl text-slate-500 mb-4"></i>
          <p className="text-slate-400 max-w-md mx-auto">Chưa có đủ dữ liệu để tạo gợi ý. Hãy đánh giá thêm nhiều phim nhé!</p>
        </div>
      )}

      {/* Bonus Section using the getRecommendByMovie API optionally */}
      {!loading && userRecs.length > 0 && (
        <div className="mt-16">
          <h3 className="text-xl font-bold text-white mb-6 pl-2 border-l-4 border-emerald-500">
            Có thể bạn cũng muốn xem (Theo phim)
          </h3>
          <MovieBasedRecs movieId={userRecs[0]?.id} />
        </div>
      )}
    </div>
  );
}

// Sub-component cho Gợi ý theo Phim
function MovieBasedRecs({ movieId }) {
  const [recs, setRecs] = useState([]);
  
  useEffect(() => {
    if(movieId) {
      ApiService.getRecommendByMovie(movieId).then(setRecs);
    }
  }, [movieId]);

  if(!recs.length) return null;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {recs.map(movie => (
        <div key={movie.id} className="bg-slate-800/80 rounded-xl p-5 flex flex-col gap-2 border border-slate-700/50 hover:border-emerald-500/50 transition-colors">
          <div className="flex justify-between items-start mb-1">
            <h4 className="font-bold text-lg text-white line-clamp-1 flex-1 pr-4">{movie.title}</h4>
            {movie.avg_rating && (
              <div className="flex items-center gap-1 text-yellow-500 text-sm font-bold bg-yellow-500/10 px-2 py-0.5 rounded">
                <i className="pi pi-star-fill text-xs"></i> {movie.avg_rating}
              </div>
            )}
          </div>
          <p className="text-sm text-slate-400 mb-2">{movie.genres ? movie.genres.join(' • ') : ''}</p>
          <div className="mt-auto bg-emerald-500/10 p-2 rounded-lg">
            <p className="text-xs text-emerald-300 line-clamp-2"><i className="pi pi-check-circle mr-1"></i>{movie.reason}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
