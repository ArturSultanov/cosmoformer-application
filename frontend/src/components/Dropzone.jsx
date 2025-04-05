import React, { useCallback, useEffect, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import './MyDropzone.css'
import { ArrowUpTrayIcon } from '@heroicons/react/24/solid'

function MyDropzone({ file, onFileAccepted, onError }) {
  const [previewUrl, setPreviewUrl] = useState(null)

  useEffect(() => {
    if (file) {
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
      return () => {
        URL.revokeObjectURL(url)
      }
    } else {
      setPreviewUrl(null)
    }
  }, [file])

  const onDrop = useCallback((acceptedFiles, fileRejections) => {
    if (acceptedFiles.length > 0) {
      onFileAccepted(acceptedFiles[0])
    }
    if (fileRejections.length > 0) {
      const reason = fileRejections[0].errors[0].message
      onError(`Error: ${reason}`)
    }
  }, [onFileAccepted, onError])

  const {
    getRootProps,
    getInputProps,
    isDragActive
  } = useDropzone({
    onDrop,
    accept: {
      'image/png': [],
      'image/jpeg': []
    },
    maxSize: 5 * 1024 * 1024, // 5MB
    multiple: false
  })

  const dropzoneClass = isDragActive ? 'dropzone dropzone-active' : 'dropzone'

  return (
    <div {...getRootProps()} className={dropzoneClass}>
      <input {...getInputProps()} />
      
      {file && previewUrl ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <img 
            src={previewUrl} 
            alt="preview" 
            style={{ maxWidth: '120px', maxHeight: '120px', marginBottom: '0.5rem' }}
          />
          <p className="dropzone-file-info">
            Selected file: {file.name}
          </p>
        </div>
      ) : (
        <div>
          <ArrowUpTrayIcon style={{ width: '24px', height: '24px' }} />
          {isDragActive
            ? <p>Drop the file here ...</p>
            : <p>Drag 'n' drop a PNG/JPEG, or click to select.</p>
          }
        </div>
      )}
    </div>
  )
}

export default MyDropzone
