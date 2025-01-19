import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './BlockGeneralAdminPage.css';

export const BlockGeneralAdminPage = () => {
  const navigate = useNavigate();
  const maxPageWidth = window.innerWidth - 100;
  const buttonHeight = 155;

  // localStorage.clear();

  const [buttons, setButtons] = useState(() => {
    const savedButtons = localStorage.getItem('buttons');
    if (savedButtons) {
      return JSON.parse(savedButtons);
    } else {
      return [{ id: 1, positionX: 0, positionY: 0, type: 'boton_mas' }];
    }
  });

  const [botonMasHistory, setBotonMasHistory] = useState(() => {
    const savedHistory = localStorage.getItem('botonMasHistory');
    if (savedHistory) {
      return JSON.parse(savedHistory);
    } else {
      return [];
    }
  });

  const [isAdmin, setIsAdmin] = useState(false);
  const [userName, setName] = useState("");

  useEffect(() => {
    const userRole = localStorage.getItem('user_role');
    setIsAdmin(userRole === 'admin');
    const getName = localStorage.getItem("name_user");
    setName(getName);
  }, []);

  useEffect(() => {
    localStorage.setItem('buttons', JSON.stringify(buttons));
    localStorage.setItem('botonMasHistory', JSON.stringify(botonMasHistory));
  }, [buttons, botonMasHistory]);

  const handleBotonMasClick = async (id) => {
    const clickedButton = buttons.find((button) => button.id === id);
    if (!clickedButton) {
      console.error('Botón no encontrado.');
      return;
    }
    const newPositionX = clickedButton.positionX + 200;
    let positionX = 0;
    if (newPositionX >= maxPageWidth) {
      positionX = 0;
    } else {
      positionX = newPositionX;
    }

    let positionY = 0;
    if (newPositionX >= maxPageWidth) {
      positionY = clickedButton.positionY + buttonHeight;
    } else {
      positionY = clickedButton.positionY;
    }

    const updatedButton = { ...clickedButton, positionX, positionY,};
  
    // Registra el historial
    setBotonMasHistory((prevHistory) => [
      ...prevHistory,
      { positionX: clickedButton.positionX, positionY: clickedButton.positionY },
    ]);
  
    // Agrega el nuevo botón
    const newButton = {
      id: buttons.length + 1,
      positionX: clickedButton.positionX,
      positionY: clickedButton.positionY,
      type: 'boton_pagina',
    };
  
    // Actualiza el estado de los botones
    setButtons((prevButtons) => [
      ...prevButtons.map((button) => (button.id === id ? updatedButton : button)),
      newButton,
    ]);
  
    // Crea el bloque en el servidor
    const newBlock = `block_${newButton.id - 1}`;
    try {
      const response = await fetch('http://127.0.0.1:5000/create-block-folder-admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: newBlock }),
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

  const handleBotonPaginaClick = async (id) => {
    if (isAdmin == false) {
      let save_name = buttons[buttons.length - 1].id - 1
      save_name = String(save_name)
      try { // Llamamos al método que crea la carpeta del bloque del usuario
        const response = await fetch('http://127.0.0.1:5000/create-block-folder-user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: userName,
            block_name: save_name, 
          }),
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
    }
    navigate(`/block_internal_admin_page/${id}`);
  };

  const removeLastButton = async () => {
    let save_name = buttons[buttons.length - 1].id - 1
    save_name = String(save_name)
    try {
      const response = await fetch('http://127.0.0.1:5000/delete-last-block-folder-admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: save_name
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
      } else {
        alert(`Error: ${data.message}`);
        return; 
      }
      setBotonMasHistory((prevHistory) => {
        if (prevHistory.length === 0) { return prevHistory; }
        const lastPosition = prevHistory[prevHistory.length - 1];
        setButtons((prevButtons) =>
          prevButtons.map((button) =>
            button.type === 'boton_mas' ? { ...button, ...lastPosition } : button
          )
        );
        return prevHistory.slice(0, -1);
      });
      setButtons((prevButtons) => prevButtons.slice(0, -1));
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }
  };

  return (
    <div className="App3">
      <div className="tittle_block_general_page">
        <h1>Bloque de preguntas</h1>
      </div>
      {buttons.map((button) => (
        (button.type === 'boton_mas' && isAdmin) || button.type !== 'boton_mas' ? (
          <button key={button.id} onClick={() => {
            if (button.type === 'boton_mas') {
              handleBotonMasClick(button.id);
            } else {
              handleBotonPaginaClick(button.id);
            }
          }
        } className="image-button" style={{transform: `translate(${button.positionX}px, ${button.positionY}px)`}}>
        <img src={require(button.type === 'boton_mas' ? '../img/icon_plus.png' : '../img/logo_ull.png')} className="user-image"/>
        </button>
        ) : null
      ))}
      {buttons.length > 1 && isAdmin && (
        <button className="button_remove_last" onClick={removeLastButton}>
          Deshacer último bloque
        </button>
      )}
    </div>
  );
};
