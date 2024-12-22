import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './QuestionPageUser.css';

export const QuestionPageUser = () => {
  const navigate = useNavigate();
  const [code, saveCode] = useState('');
  const [inputCode, setInputCode] = useState('');
  const [file, setFile] = useState(null);

  const UploadFile = async () => {
    if (!file) {
      alert('Por favor selecciona un archivo para subir.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload-file', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message); // Mensaje del servidor
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }
  };

  const GoToUser = () => {
    navigate('/'); 
  };

  
  var tittle = "Titulo"
  var description = "bla bla"

  return (
    <div className="App2">
      <div className="title-box">
        <h1>{tittle}</h1>
      </div>
      <div className="description">
        <h2>{description}</h2>
      </div>
        
      <div className="button-container-first-line">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} className="file-input"/>
        <button className="button_submit" onClick={UploadFile}>
          Subir archivo
        </button>
        
      </div>
      <div className="button-container-second-line" onClick={GoToUser}>
        <button className="button_submit">
          Hecho
        </button>
      </div>
    </div>
  );
  
};
