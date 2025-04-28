import React, { useState } from 'react';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file to upload');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      alert('File uploaded successfully!');
    } catch (err) {
      setError(err.message);
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Upload a File</h1>
      
      <input 
        type="file" 
        onChange={handleFileChange} 
        style={styles.input}
      />
      
      <button 
        onClick={handleUpload} 
        disabled={uploading} 
        style={{ 
          ...styles.button, 
          backgroundColor: uploading ? '#ccc' : '#007BFF', 
          cursor: uploading ? 'not-allowed' : 'pointer' 
        }}
      >
        {uploading ? 'Uploading...' : 'Upload File'}
      </button>

      {uploading && (
        <div style={styles.progressContainer}>
          <progress value={uploadProgress} max="100" style={styles.progress}></progress>
          <p>{uploadProgress}%</p>
        </div>
      )}

      {error && <p style={styles.error}>{error}</p>}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '600px', // Match the width of the Chat component
    margin: '50px auto',
    padding: '20px',
    border: '1px solid #eee',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    textAlign: 'center',
    backgroundColor: '#fafafa',
  },
  title: {
    marginBottom: '20px',
    color: '#333',
  },
  input: {
    marginBottom: '20px',
    width: '100%',
  },
  button: {
    padding: '10px 20px',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    fontSize: '16px',
  },
  progressContainer: {
    marginTop: '20px',
  },
  progress: {
    width: '100%',
    height: '20px',
  },
  error: {
    color: 'red',
    marginTop: '15px',
  },
};

export default FileUpload;
