import React, { useState, useEffect, createContext, useContext} from 'react';
import { useNavigate } from 'react-router-dom';
import './BlockGeneralAdminPage.css';

export const BlockGeneralAdminPage = () => {
  const navigate = useNavigate();
  const maxPageWidth = window.innerWidth - 100;
  const buttonHeight = 155;

  const userContext = createContext('user');

  // localStorage.clear();

  const [buttons, setButtons] = useState(() => {
    const savedButtons = localStorage.getItem('buttons');
    if (savedButtons) {
      return JSON.parse(savedButtons);
    } else {
      return [{ id: 1, positionX: 0, positionY: 0, type: "boton_mas", block_name: "default"}];
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
  const [isMonitor, setIsMonitor] = useState(false);
  const [isTemporalyUser, setIsTemporalyUser] = useState(false);
  const [userName, setName] = useState("");
  const [saveRol, setSaveRol] = useState("");

  useEffect(() => {
    const userRole = localStorage.getItem("user_role");
    setIsAdmin(userRole === "admin");
    setIsMonitor(userRole === "monitor")
    const getName = localStorage.getItem("name_user");
    setName(getName);
    setSaveRol(userRole);
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

    let block_name = `block_${buttons.length}`;

  
    localStorage.setItem('current_block_name', block_name);
     
  
    // Agrega el nuevo botón
    const newButton = {
      id: buttons.length + 1,
      positionX: clickedButton.positionX,
      positionY: clickedButton.positionY,
      type: "boton_pagina",
      block_name: block_name,
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

    // Registrar la información en el JSON de datos de la APP
    const button_id = newButton.id - 1
    try {
      const response = await fetch('http://127.0.0.1:5000/regist-block-admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: button_id }),
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

    // Registrar la información en el JSON de los botones de bloque
    try {
      const response = await fetch('http://127.0.0.1:5000/regist-block-button', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: button_id,
          positionX: newButton.positionX,
          positionY: newButton.positionY,
          type: newButton.type,
          block_name: newButton.block_name, 
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


  };

  const handleBotonPaginaClick = async (id) => {
    if ((isAdmin === false) && (isMonitor === false)) {
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
    navigate(`/block_internal_admin_page/${buttons[buttons.length - 1].block_name}`);
  };

  const removeLastButton = async () => {
    let save_name = buttons[buttons.length - 1].id - 1
    save_name = String(save_name)
    try { // Eliminar la carpeta del último bloque
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

    let button_id =  buttons[buttons.length - 1].id - 1
    

    try { // Llamamos al método que borra del registro al bloque del json de datos de la APP
      const response = await fetch('http://127.0.0.1:5000/delete-last-block-json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: button_id 
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

    try { // Llamamos al método que borra del registro al bloque del json de registro de botones
      const response = await fetch('http://127.0.0.1:5000/delete-last-block-button-of-json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: button_id 
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
  };

  const ChangePermission = () => {
    if (isTemporalyUser === false) {
      if (isAdmin === true) { setIsAdmin(false) }
      if (isMonitor === true) { setIsMonitor(false) }
      setIsTemporalyUser(true) 
    } else {
      setIsTemporalyUser(false);
      if (saveRol === "admin") { setIsAdmin(true) }
      if (saveRol === "monitor") { setIsMonitor(true) }
    }
  }

  return (
    <div className="App3">
      <div className="tittle_block_general_page">
        <h1>Bloque de preguntas</h1>
      </div>
      {buttons.map((button) => (
        (button.type === 'boton_mas' && ((isAdmin === true) || (isMonitor === true))) || button.type !== 'boton_mas' ? (
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
      {buttons.length > 1 && ((isAdmin === true) || (isMonitor === true)) && (
        <button className="button_remove_last" onClick={removeLastButton}>
          Deshacer último bloque
        </button>
      )}
      {buttons.length > 1 && ((isAdmin === true) || (isMonitor === true)) && (
        <button className="button_change_to_admin_or_monitor" onClick={ChangePermission}>
          Probar cómo usuario
        </button>
      )}
      {buttons.length > 1 && (isTemporalyUser == true) && (
        <button className="button_change_to_admin_or_monitor" onClick={ChangePermission}>
          Volver al rol anterior
        </button>
      )}
    </div>
  );
};
