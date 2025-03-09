import React, { useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import './BlockGeneralAdminPage.css';
import { route_to_server } from '../App';

export const BlockGeneralAdminPage = () => {
  const navigate = useNavigate();
  const maxPageWidth = window.innerWidth - 100;
  const buttonHeight = 155;

  const [saveJson, setSaveJson] = useState();

  useEffect(() => {
    const getJsonData = async () => {
      try {
        const response = await fetch(route_to_server + 'get-data-blocks-buttons-json');
        const data = await response.json();
        if (response.ok) {
          setSaveJson(JSON.parse(data.data));  // Guardamos el contenido en el estado
        } else {
          console.error(`Error: ${data.error}`);
        }
      } catch (error) {
        console.error('Error al obtener los datos del servidor', error);
      }
    };
    getJsonData();
  }, []);

  // localStorage.clear();

  const [buttons, setButtons] = useState([]);

  useEffect(() => {
    if (!saveJson) { return; }
    let save_buttons = [];
    if (saveJson.length !== 0) {
      save_buttons = saveJson;
      let lastButton = save_buttons[save_buttons.length - 1];
      const newPositionX = lastButton.positionX + 200;
      let positionX = 0;
      if (newPositionX >= maxPageWidth) {
        positionX = 0;
      } else {
        positionX = newPositionX;
      }
      let positionY = 0;
      if (newPositionX >= maxPageWidth) {
        positionY = lastButton.positionY + buttonHeight;
      } else {
        positionY = lastButton.positionY;
      }
      save_buttons.push({ id: lastButton.id + 1, positionX: positionX, positionY: positionY, type: "boton_mas", block_name: "default"});
    } else {
      save_buttons.push({ id: 1, positionX: 0, positionY: 0, type: "boton_mas", block_name: "default"});
    }
    setButtons(save_buttons);
  }, [saveJson]); 

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

  const handlePlusButtonClick = async (id) => {
    const clickedButton = buttons.find((button) => button.id === id); // Confirmamos que es el botón que estamos pulsando
    const newPositionX = clickedButton.positionX + 200; // Miramos si se puede avanzar más del límite de la pantalla
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

    // Guardamos el nombre del bloque actual
    let block_name = `block_${buttons.length}`;
    localStorage.setItem('current_block_name', block_name);
  
    // Datos del nuevo botón
    const newButton = {
      id: buttons.length + 1,
      positionX: clickedButton.positionX,
      positionY: clickedButton.positionY,
      type: "boton_pagina",
      block_name: block_name,
      default_image: "./img/logo_ull.png"
    };
  
    // Crea el bloque en el servidor
    const newBlock = `block_${newButton.id - 1}`;
    try {
      const response = await fetch(route_to_server + 'create-block-folder-admin', {
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

    try {
      const response = await fetch(route_to_server + 'create-block-folder-admin-for-puntuations', {
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
      const response = await fetch(route_to_server + 'regist-block-admin', {
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
      const response = await fetch(route_to_server + 'regist-block-button', {
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
          default_image: newButton.default_image,
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

    window.location.reload();
  };

  const handleNewPageButtonClick = async (id) => {
    if ((isAdmin === false) && (isMonitor === false)) {
      let save_name = id - 1
      save_name = String(save_name)
      try { // Llamamos al método que crea la carpeta del bloque del usuario
        const response = await fetch(route_to_server + 'create-block-folder-user', {
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

      try { // Llamamos al método que crea la carpeta del bloque del usuario
        const response = await fetch(route_to_server + 'create-register-folder-user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
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

      try { // Llamamos al método que crea la carpeta del bloque del usuario
        const response = await fetch(route_to_server + 'regist-user', {
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
          if (response.status !== 500) {
            alert(`Error: ${data.message}`);
          }
        }
      } catch (error) {
        alert('Error al conectar con el servidor.');
        console.error(error);
      }

    }
    navigate(`/block_internal_admin_page/block_${id}`);
  };

  const removeLastButton = async () => {
    let save_name = buttons[buttons.length - 1].id - 1
    save_name = String(save_name)
    try { // Eliminar la carpeta del último bloque
      const response = await fetch(route_to_server + 'delete-last-block-folder-admin', {
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
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }

    try { // Eliminar la carpeta de puntuaciones del último bloque
      const response = await fetch(route_to_server + 'delete-last-block-folder-admin-for-puntuations', {
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
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }


    let button_id =  buttons[buttons.length - 1].id - 1
    try { // Llamamos al método que borra del registro al bloque del json de datos de la APP
      const response = await fetch(route_to_server + 'delete-last-block-json', {
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
      const response = await fetch(route_to_server + 'delete-last-block-button-of-json', {
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
      const response = await fetch(route_to_server + '/delete-block-in-question-button-json', {
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
        if (response.status !== 500) {
          alert(`Error: ${data.message}`);
        }
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }

    try { // Eliminar la carpeta del último bloque
      const response = await fetch(route_to_server + 'delete-last-student-register', {
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
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }

    window.location.reload();
  };

  const ChangePermission = () => {
    if (isTemporalyUser === false) {
      if (isAdmin === true) { setIsAdmin(false) }
      if (isMonitor === true) { setIsMonitor(false) }
      setIsTemporalyUser(true) 
      alert("Permisos cambiados a usuario")
    } else {
      setIsTemporalyUser(false);
      if (saveRol === "admin") { 
        setIsAdmin(true)
        alert("Permisos de administrador recuperados") 
      }
      if (saveRol === "monitor") { 
        setIsMonitor(true) 
        alert("Permisos de monitor recuperados")
      }
    }
  }

  const MoveToUserLogin = () => {
    navigate('/');
  };

  const MoveToAdminLogin = () => {
    navigate('/admin_page_user');
  };

  return (
    <div className="App3">
      <div className="tittle_block_general_page">
        <h1>Bloque de preguntas</h1>
      </div>
      {buttons.map((button) => (
        (button.type === 'boton_mas' && ((isAdmin === true) || (isMonitor === true))) || button.type !== 'boton_mas' ? (
          <button key={button.id} onClick={() => {
            if (button.type === 'boton_mas') {
              handlePlusButtonClick(button.id);
            } else {
              handleNewPageButtonClick(button.id);
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
      {buttons.length > 1 && (isTemporalyUser === true) && (
        <button className="button_change_to_admin_or_monitor_activated" onClick={ChangePermission}>
          Volver al rol anterior
        </button>
      )}
      {((isAdmin === true) || (isMonitor === true) || (isTemporalyUser === true)) && (
        <button className="button_move_previous_page" onClick={MoveToAdminLogin}>
          Volver a la página de Inicio
        </button>
      )}
      {((isAdmin === false) && (isMonitor === false) && (isTemporalyUser === false)) && (
        <button className="button_move_previous_page" onClick={MoveToUserLogin}>
          Volver a la página anterior
        </button>
      )}
    </div>
  );
};
