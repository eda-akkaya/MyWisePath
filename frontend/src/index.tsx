import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Uygulamanızda performans ölçümü yapmak istiyorsanız, bir fonksiyon geçin
// sonuçları kaydetmek için (örneğin: reportWebVitals(console.log))
// veya analitik endpoint'ine gönderin. Daha fazla bilgi: https://bit.ly/CRA-vitals
reportWebVitals();
