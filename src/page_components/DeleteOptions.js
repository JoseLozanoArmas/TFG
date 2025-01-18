import React from 'react';
import { useNavigate } from 'react-router-dom';
import './DeleteOptions.css';

export const DeleteOptions = () => {
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

  const resetBlocksData = async () => {
    try {
      const response = await fetch('http://localhost:5000/reset-blocks-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        alert(data.message); 
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`); 
      }
    } catch (error) {
      alert(`Error de conexión: ${error.message}`); 
    }
  };
  
  const resetUsersRegisteredData = async () => {
    try {
      const response = await fetch('http://localhost:5000/reset-users-registered-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        alert(data.message); 
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`); 
      }
    } catch (error) {
      alert(`Error de conexión: ${error.message}`); 
    }
  };
  
  return (
    <div className="delete_options_page_admin">
      <div className="tittle_delete_page">
        <h1>Opciones de borrado</h1>
      </div>
    <button className="button_reset_student_information" onClick={resetUsers}>
      Borrar toda la información de los estudiantes
    </button>
    <button className="button_reset_student_information" onClick={resetBlocksData}>
      Borrar toda la información de los bloques de preguntas
    </button>
  <button className="button_reset_student_information" onClick={resetUsersRegisteredData}>
    Borrar todos los usuarios registrados
  </button>
</div>

  );
}