import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './components/navbar/Navbar.jsx'
import { BrowserRouter } from 'react-router'
import Body from './components/Body.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
function App() {
  return (
    <div className="h-screen flex flex-col">
      
    <BrowserRouter>
    <AuthProvider>
     <Navbar/>
     <div className="flex-1 overflow-y-auto ">
        <Body />
      </div>
    </AuthProvider>
     </BrowserRouter>
     
    </div>
  )
}

export default App
