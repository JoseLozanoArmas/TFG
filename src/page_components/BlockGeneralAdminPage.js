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

  useEffect(() => {
    const userRole = localStorage.getItem('user_role');
    setIsAdmin(userRole === 'admin');
  }, []);

  useEffect(() => {
    localStorage.setItem('buttons', JSON.stringify(buttons));
    localStorage.setItem('botonMasHistory', JSON.stringify(botonMasHistory));
  }, [buttons, botonMasHistory]);

  const handleBotonMasClick = (id) => {
    setButtons((prevButtons) => {
      const updatedButtons = prevButtons.map((button) => {
        if (button.id === id) {
          setBotonMasHistory((prevHistory) => [...prevHistory, { positionX: button.positionX, positionY: button.positionY },]);
          const newPositionX = button.positionX + 200;
          if (newPositionX >= maxPageWidth) {
            return {...button, positionX: 0, positionY: button.positionY + buttonHeight,};
          }
          return { ...button, positionX: newPositionX };
        }
        return button;
      });
      const clickedButton = prevButtons.find((button) => button.id === id);
      const newButton = { id: prevButtons.length + 1, positionX: clickedButton.positionX, positionY: clickedButton.positionY, type: 'boton_pagina',};
      return [...updatedButtons, newButton];
    });
  };

  const handleBotonPaginaClick = (id) => {
    navigate(`/block_internal_admin_page/${id}`);
  };

  const removeLastButton = () => {
    setButtons((prevButtons) => {
      if (prevButtons.length >= 1) {
        setBotonMasHistory((prevHistory) => {
          const lastPosition = prevHistory[prevHistory.length - 1];
          setButtons((updatedButtons) =>
            updatedButtons.map((button) => {
              if (button.type === 'boton_mas') {
                return [{ ...button, ...lastPosition }];
              } else {
                return button;
              }
            })
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
