import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './index.css';

// PrimeReact Styles
import "primereact/resources/themes/lara-dark-indigo/theme.css";  // Theme dark mode
import "primereact/resources/primereact.min.css";                  // Core CSS
import "primeicons/primeicons.css";                                // Icons

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
