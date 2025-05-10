import React from 'react'
import { Route,Router,Routes } from 'react-router'
import Home from '../pages/Home'
import Login from '../pages/Login'
import Find from '../pages/Find'
import Contact from '../pages/Contact'
import Result from '../pages/Result'
import Specs from '../pages/Specs'
import ProtectedRoute from '../routes/ProtectedRoute'
const Body = () => {
  return (
    <div  className='body relative h-full w-screen overflow-y-auto'>
    <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/login' element={<Login/>}/>
        <Route path='/find' element={<ProtectedRoute><Find/></ProtectedRoute>}/>
        <Route path='/contact' element={<ProtectedRoute><Contact/></ProtectedRoute>}/>
        <Route path='/results' element={<ProtectedRoute><Result/></ProtectedRoute>}/>
        <Route path='/specs' element={<ProtectedRoute><Specs/></ProtectedRoute>}/>

    </Routes>
      
    </div>
  )
}

export default Body
