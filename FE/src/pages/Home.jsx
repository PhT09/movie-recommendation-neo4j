import React, { useState, useContext } from 'react';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';

export default function Home() {
  const [inputValue, setInputValue] = useState('');
  const { login } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      login(inputValue.trim());
      navigate('/rating');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh]">
      <div className="max-w-md w-full bg-slate-800 p-8 rounded-2xl shadow-2xl text-center border border-slate-700/50 backdrop-blur-sm">
        <div className="mb-6 flex justify-center">
          <div className="h-16 w-16 bg-indigo-600 rounded-full flex items-center justify-center shadow-lg shadow-indigo-600/30">
            <i className="pi pi-video text-2xl text-white"></i>
          </div>
        </div>
        <h1 className="text-4xl font-bold text-white mb-2 tracking-tight">MovieNeo</h1>
        <p className="text-slate-400 mb-8 text-sm">Hệ thống gợi ý phim thông minh</p>
        
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <div className="relative">
            <span className="p-input-icon-left w-full block">
              <i className="pi pi-user text-slate-400 z-10" />
              <InputText 
                placeholder="Nhập UserID của bạn" 
                value={inputValue} 
                onChange={(e) => setInputValue(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-white p-3 pl-10 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all placeholder:text-slate-500 font-sans"
              />
            </span>
          </div>
          <Button 
            label="Vào hệ thống" 
            icon="pi pi-arrow-right" 
            iconPos="right" 
            className="w-full p-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 hover:-translate-y-0.5 border-none font-semibold transition-all shadow-lg shadow-indigo-600/20 text-white flex justify-center items-center gap-2"
            type="submit"
          />
        </form>
      </div>
    </div>
  );
}
