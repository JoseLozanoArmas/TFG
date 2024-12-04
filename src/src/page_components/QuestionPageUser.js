import React, { useState } from 'react';
import './QuestionPageUser.css';

export const QuestionPageUser = () => {
  const [code, saveCode] = useState('');
  const [inputCode, setInputCode] = useState('');

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
      <div className="input-box2"> 
        <textarea className='code_input' value={code} onChange={(e) => saveCode(e.target.value)} placeholder="Escribe algo aquí..." ></textarea>
      </div>
        <button className='button_submit' onClick={sendTextToServer}>Enviar Texto al Servidor</button>
    </div>
  );
};
