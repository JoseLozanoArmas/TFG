import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './GeneralUserPage.css';
import { route_to_server } from '../App';

export const GeneralUserPage = () => {
  const navigate = useNavigate();
  const maxPageWidth = window.innerWidth - 100;
  const userHeight = 155;
  const [isAdmin, setIsAdmin] = useState(false);

  // localStorage.clear();
  
  useEffect(() => {
  const userRole = localStorage.getItem('user_role');
    setIsAdmin(userRole === 'admin');
  }, []);

  const [saveJson, setSaveJson] = useState();

  useEffect(() => {
    const getJsonData = async () => {
      try {
        const response = await fetch(route_to_server + 'get-info-users-json'); // Recibir la información del JSON de registro
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


  const [users, setUsers] = useState([]);

  useEffect(() => { // Establecer las entradas de los usuarios en base a la información recibida por parte del JSON
    if (!saveJson) { return; }
    let save_users = [];
    if (saveJson.length !== 0) {
      save_users = saveJson;
      let lastUser = save_users[save_users.length - 1];
      const newPositionX = lastUser.positionX + 200;
      let positionX = 0;
      if (newPositionX >= maxPageWidth) {
        positionX = 0;
      } else {
        positionX = newPositionX;
      }
      let positionY = 0;
      if (newPositionX >= maxPageWidth) {
        positionY = lastUser.positionY + userHeight;
      } else {
        positionY = lastUser.positionY;
      }
      save_users.push({ id: lastUser.id + 1, positionX: positionX, positionY: positionY, type: "button_plus"});
    } else {
      save_users.push({ id: 0, positionX: 0, positionY: 0, type: "button_plus"});
    }
    setUsers(save_users);
  }, [saveJson, maxPageWidth]); 

  const handleButtonPlusClick = async (id) => { // Crear nuevos usuarios
    const clickedUser = users.find((user) => user.id === id);
    if (!clickedUser) {
      console.error('Botón no encontrado.');
      return;
    }
  
    const newUser = {
      id: users.length + 1,
      positionX: clickedUser.positionX,
      positionY: clickedUser.positionY,
      type: 'user',
    };

    navigate(`/creation_user/${newUser.id}`);
  };

  const removeLastUser = async () => {
    try {
      const response = await fetch(route_to_server + 'remove-last-user', { // Eliminar el último usuario registrado
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
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

  const handleButtonUserClick = async (id) => {
    navigate(`/creation_user/${id}`)
  }

  return (
    <div className="App3">
      <div className="tittle_block_general_page">
        <h1>Bloque de usuarios</h1>
      </div>
      {users.map((user) => (
        (user.type === 'button_plus' && isAdmin) || user.type !== 'button_plus' ? (
          <button key={user.id} onClick={() => {
            if (user.type === 'button_plus') {
              handleButtonPlusClick(user.id);
            } else {
              handleButtonUserClick(user.id);
            }
          }
        } className="image-button" style={{transform: `translate(${user.positionX}px, ${user.positionY}px)`}}>
        <img src={require(user.type === 'button_plus' ? '../img/icon_plus.png' : '../img/user_img.png')} className="user-image" alt=""/>
        <span className="label-name"> {user.username} </span>
        </button>
        ) : null
      ))} 
      {users.length > 2 && isAdmin && (
        <button className="button_remove_last" onClick={removeLastUser}>
          Deshacer último usuario
        </button>
      )}
    </div>
  );

}