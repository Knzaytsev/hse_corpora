import React from 'react';
import ReactDOM from 'react-dom/client';

import 'bootstrap/dist/css/bootstrap.min.css';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import AboutPage from './About';
import Navigation from './navbar';
import SearchableTable from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <Router>
      <Navigation />
        <Routes>
          <Route path='/' element={<SearchableTable />} />
          <Route path='/about' element={<AboutPage />} />
          </Routes>
      </Router>
  </React.StrictMode>
);

