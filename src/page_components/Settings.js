import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Settings.css';

export const Settings = () => {
  const navigate = useNavigate();

  const resetUsers = async () => {
    try {
      const response = await fetch('http://localhost:5000/reset-users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        alert(data.message); // Muestra un mensaje de éxito
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`); // Muestra un mensaje de error
      }
    } catch (error) {
      alert(`Error de conexión: ${error.message}`); // Manejo de errores de conexión
    }
  };
  
  return (
    <div className="settings_page_admin">
      <button className="button_reset_ranking" onClick={resetUsers}>Reset</button>
    </div>
  );
}