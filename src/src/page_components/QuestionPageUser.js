import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './QuestionPageUser.css';

export const QuestionPageUser = () => {
  const navigate = useNavigate();
  const [code, saveCode] = useState('');
  const [inputCode, setInputCode] = useState('');

  const UploadFile = () => {
    console.log("pendiente")
  }

  const GoToUser = () => {
    navigate('/'); 
  };

  const sendTextToServer = async () => {
    if (!code.trim()) {
      alert('No se introdujo ningún código. Por favor rellene la caja de entrada con su código');
      return;
    }
  
    try {
      const response = await fetch('http://127.0.0.1:5000/save-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: code }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        alert(data.message); 
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }
  };
  

  return (
    <div className="App2">
      <div className="title-box">
        <h1>Título</h1>
      </div>
        <textarea className="code_input"
          value={code}
          onChange={(e) => saveCode(e.target.value)}
          placeholder="Introduce tu código"
        ></textarea>
      <div className="button-container-first-line">
        <button className="button_submit" onClick={UploadFile}>
          Subir archivo
        </button>
        <button className="button_submit" onClick={sendTextToServer}>
          Enviar Código
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
