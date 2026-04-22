import React, { useContext } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { UserContext } from '../context/UserContext';

export default function Navbar() {
  const { userId, logout } = useContext(UserContext);
  const location = useLocation();
  const navigate = useNavigate();

  if (!userId) return null; // Không hiện navbar nếu chưa đăng nhập

  const navLinks = [
    { name: 'Đánh giá', path: '/rating', icon: 'pi pi-star' },
    { name: 'Gợi ý', path: '/recommendation', icon: 'pi pi-compass' }
  ];

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
            <i className="pi pi-video text-white text-sm"></i>
          </div>
          <span className="font-bold text-xl text-white tracking-tight">MovieNeo</span>
        </div>

        <div className="flex gap-1 md:gap-4">
          {navLinks.map((link) => {
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-2 rounded-xl flex items-center gap-2 transition-all ${
                  isActive 
                    ? 'bg-indigo-500/10 text-indigo-400 font-semibold' 
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                <i className={`${link.icon} ${isActive ? 'text-indigo-400' : ''}`}></i>
                <span className="hidden md:inline">{link.name}</span>
              </Link>
            );
          })}
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-slate-800 rounded-lg border border-slate-700">
            <i className="pi pi-user text-slate-400 text-xs"></i>
            <span className="text-sm font-medium text-slate-300">{userId}</span>
          </div>
          <button 
            onClick={handleLogout}
            className="w-10 h-10 rounded-xl bg-red-500/10 text-red-500 hover:bg-red-500 hover:text-white flex items-center justify-center transition-all"
            title="Đăng xuất"
          >
            <i className="pi pi-sign-out"></i>
          </button>
        </div>
      </div>
    </nav>
  );
}
