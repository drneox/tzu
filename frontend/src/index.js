import React from "react";
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ChakraProvider } from "@chakra-ui/react";

import Header from "./components/Header";
import Footer from "./components/Footer";
import Todos from "./components/Todos";
import ListInformationSystem from "./components/List";
import Index from "./components/Index";
import Analysis from "./components/Analysis";
import CreateInformationSystem from "./components/CreateInformationSystem";
import UploadDiagram from "./components/UploadDiagram";

function App() {
  return (

    <ChakraProvider>
      <Header/>
      <Routes>
        <Route path="/" element={ <Index /> } />
        <Route path="/analysis/:id" element={ <Analysis /> } />
        <Route path="/create" element={ <CreateInformationSystem /> } />
        <Route path="/upload/:id" element={ <UploadDiagram /> } />
      </Routes>
      <Footer/>
    </ChakraProvider>
  )
}

const container = document.getElementById("root")
const root = createRoot(container)
root.render(
  <BrowserRouter>

<App tab="home" />
  </BrowserRouter>
)