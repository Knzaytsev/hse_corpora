import React from 'react';
import ReactDOM from 'react-dom/client';

import 'bootstrap/dist/css/bootstrap.min.css';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import AboutPage from './About';
import Navigation from './navbar';
import SearchableTable from './App';
import MistakesSearch from './mistake-search';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <Router>
      <Navigation />
        <Routes>
          <Route path='/' element={<AboutPage />} />
          <Route path='/general-search' element={<SearchableTable />} />
          <Route path='/mistakes-search' element={<MistakesSearch />} />
          </Routes>
      </Router>
  </React.StrictMode>
);

