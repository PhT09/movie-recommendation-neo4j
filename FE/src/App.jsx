import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { UserProvider, UserContext } from './context/UserContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Rating from './pages/Rating';
import Recommendation from './pages/Recommendation';

// Route bảo vệ, tự động chuyển hướng nếu chưa đăng nhập
const ProtectedRoute = ({ children }) => {
  const { userId } = useContext(UserContext);
  const location = useLocation();

  if (!userId) {
    return <Navigate to="/" state={{ from: location }} replace />;
  }

  return children;
};

// Route điều hướng khỏi trang chủ nếu đã đăng nhập
const PublicRoute = ({ children }) => {
  const { userId } = useContext(UserContext);
  
  if (userId) {
    return <Navigate to="/rating" replace />;
  }

  return children;
};

function App() {
  return (
    <UserProvider>
      <Router>
        <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30">
          <Navbar />
          <main>
            <Routes>
              <Route path="/" element={
                <PublicRoute>
                  <Home />
                </PublicRoute>
              } />
              <Route path="/rating" element={
                <ProtectedRoute>
                  <Rating />
                </ProtectedRoute>
              } />
              <Route path="/recommendation" element={
                <ProtectedRoute>
                  <Recommendation />
                </ProtectedRoute>
              } />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;
