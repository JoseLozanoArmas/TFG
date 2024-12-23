import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './BlockGeneralAdminPage.css';

export const BlockGeneralAdminPage = () => {
  const navigate = useNavigate();
  const maxPageWidth = window.innerWidth - 100;
  const buttonHeight = 155;

  const [buttons, setButtons] = useState([
    { id: 1, positionX: 0, positionY: 0, type: 'boton_mas' },
  ]);

  const [botonMasHistory, setBotonMasHistory] = useState([]);

  const handleBotonMasClick = (id) => {
    setButtons((prevButtons) => {
      const updatedButtons = prevButtons.map((button) => {
        if (button.id === id) {
          setBotonMasHistory((prevHistory) => [
            ...prevHistory,
            { positionX: button.positionX, positionY: button.positionY },
          ]);
          const newPositionX = button.positionX + 200;
          if (newPositionX >= maxPageWidth) {
            return {
              ...button,
              positionX: 0,
              positionY: button.positionY + buttonHeight,
            };
          }
          return { ...button, positionX: newPositionX };
        }
        return button;
      });
      const clickedButton = prevButtons.find((button) => button.id === id);
      const newButton = {
        id: prevButtons.length + 1,
        positionX: clickedButton.positionX,
        positionY: clickedButton.positionY,
        type: 'boton_pagina',
      };
      return [...updatedButtons, newButton];
    });
  };

  const handleBotonPaginaClick = () => {
    navigate('/block_internal_admin_page');
  };

  const removeLastButton = () => {
    setButtons((prevButtons) => {
      if (prevButtons.length > 1) {
        setBotonMasHistory((prevHistory) => {
          const lastPosition = prevHistory[prevHistory.length - 1];
          setButtons((updatedButtons) =>
            updatedButtons.map((button) => button.type === 'boton_mas' ? { ...button, ...lastPosition } : button)
          );
          return prevHistory.slice(0, -1); 
        });
      }
      return prevButtons.slice(0, -1); 
    });
  };

  return (
    <div className="App3">
      <div className="tittle_block_general_page">
        <h1>Bloque de preguntas</h1>
      </div>
      {buttons.map((button) => (
        <button key={button.id} onClick={button.type === 'boton_mas' ? () => handleBotonMasClick(button.id) : handleBotonPaginaClick} className="image-button" style={{transform: `translate(${button.positionX}px, ${button.positionY}px)`,}}>
          <img src={require(button.type === 'boton_mas' ? '../img/icon_plus.png' : '../img/logo_ull.png')} alt={button.type} className="user-image"/>
        </button>
      ))}
      {buttons.length > 1 && (
        <button className="button_remove_last" onClick={removeLastButton}>
          Deshacer último bloque
        </button>
      )}
    </div>
  );
};
