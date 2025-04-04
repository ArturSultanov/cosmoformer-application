import { useState } from 'react'
import galaxyLogo from '/galaxy.svg'
import './App.css'
import MyDropzone from '@/components/Dropzone'

function App() {

  return (
    <>
      <h1>Galaxy class app</h1>
      <div>
        <img src={galaxyLogo} className="logo" alt="Vite logo" />
      </div>
      <MyDropzone className='p-16 mt-10 border border-neutral-200' />
    </>
  )
}

export default App
