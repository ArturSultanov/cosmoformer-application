import React, { useState } from 'react'
import axios from 'axios'
import galaxyLogo from '/galaxy.svg'
import './App.css'
import MyDropzone from '@/components/Dropzone'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Called by MyDropzone when a file is accepted
  const onFileAccepted = (file) => {
    setSelectedFile(file)
    setResult('')
    setError('')
  }

  // Called by MyDropzone when there's a validation error
  const onDropzoneError = (msg) => {
    setError(msg)
  }

  // Clear button resets all relevant states
  const handleClear = () => {
    setSelectedFile(null)
    setResult('')
    setError('')
  }

  // Submit button triggers the POST /inference request
  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('No file selected')
      return
    }
    setLoading(true)
    setResult('')
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      // const response = await axios.post(
      //   'http://localhost:8000/inference',
      //   formData,
      //   {
      //     headers: {
      //       'Content-Type': 'multipart/form-data'
      //     }
      //   }
      // )

      // TODO: remove - this is just for testing purposes
      const response = await axios.post(
        '/api/inference',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )

      // Expected JSON: { "predicted_class": "string" }
      setResult(response.data.predicted_class)
    } catch (err) {
      console.error(err)
      setError('Error processing the image')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h1>Galaxy class app</h1>
      <div>
        <img src={galaxyLogo} className="logo" alt="Galaxy logo" />
      </div>

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Predicted Class: {result}</h3>
        </div>
      )}

      {error && (
        <p style={{ color: 'red', marginTop: '20px' }}>
          {error}
        </p>
      )}

      <MyDropzone
        file={selectedFile}
        onFileAccepted={onFileAccepted}
        onError={onDropzoneError}
      />

      <div style={{ marginTop: '20px' }}>
        <button onClick={handleSubmit} disabled={!selectedFile || loading}>
          {loading ? 'Submitting...' : 'Submit'}
        </button>
        <button
          onClick={handleClear}
          disabled={!selectedFile && !error}
          style={{ marginLeft: '10px' }}
        >
          Clear
        </button>
      </div>
    </>
  )
}

export default App
