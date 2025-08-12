import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ChakraProvider } from '@chakra-ui/react';
import './App.css';

// Importar componentes
import Header from './components/Header';
import Footer from './components/Footer';
import Index from './components/Index';
import List from './components/List';
import Analysis from './components/Analysis';

function App() {
  return (
    <ChakraProvider>
      <Router>
        <div className="App">
          <Header />
          <main>
            <Routes>
              <Route path="/" element={<Index />} />
              <Route path="/list" element={<List />} />
              <Route path="/analysis/:id" element={<Analysis />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </ChakraProvider>
  );
}

export default App;
