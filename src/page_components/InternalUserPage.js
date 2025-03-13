import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './InternalUserPage.css';
import default_user_image from '../img/user_img.png';
import { route_to_server } from '../App';

export const InternalUserPage = () => {
  const navigate = useNavigate();
  const maxPageWidth = window.innerWidth - 100;
  const userHeight = 155;
  const offsetX = 200;
  const { id } = useParams();
  const [currentLogo, setCurrentLogo] = useState(() => {
    const savedLogo = localStorage.getItem(`logo_${id}`);
    if (savedLogo) {
      return JSON.parse(savedLogo);
    } else {
      return default_user_image;
    }
  });

  // localStorage.clear();

  const [userName, setUserName] = useState(""); 
  const [password, setPassword] = useState(""); 
  const [rol, setRol] = useState(""); 

  useEffect(() => {
    const getJsonData = async () => {
      try {
        const response = await fetch(route_to_server + 'get-user-information', { // Recibimos la información del usuario en cuestión
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: id
          }),
        });
        const data = await response.json();
        if (response.ok) {
          let save_info = JSON.parse(data.data)
          setUserName(save_info["username"]);
          setPassword(save_info["password"]);
          setRol(save_info["rol"]);
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (error) {
        alert('Error al conectar con el servidor.');
        console.error(error); 
      }
    };
    getJsonData();
  }, [id]);

  const handleLogoChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const newLogo = URL.createObjectURL(file);
      setCurrentLogo(newLogo);
    }
  };

  const triggerFileInput = () => {
    document.getElementById("file-input").click();
  };

  const handleUserNameChange = (event) => {
    setUserName(event.target.value); 
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value); 
  };

  const handleRolChange = (event) => {
    setRol(event.target.value); 
  };

  const checkAllInformation = async () => { // Comprobamos que todo sea correcto para poder añadir un usuario
    if (!userName.trim()) { 
      alert("Por favor introduzca un nombre al usuario");
      return;
    }

    if (!password.trim()) { 
      alert("Por favor introduzca una contraseña al usuario");
      return;
    }

    if (!rol.trim()) { 
      alert("Por favor introduzca un rol al usuario");
      return;
    }

    try {
      const response = await fetch(route_to_server + 'add-new-user', { // Añadir nuevos usuarios
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: userName,
          password: password,
          rol: rol,
          offsetX: offsetX,
          offsetY: userHeight,
          limit_position: maxPageWidth
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        navigate('/general_users')
      } else {
        alert(`Error: ${data.message}`);
        return; 
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }
  };

  return (
    <div className="App_creation_user_page">
      <div className="tittle_creation_user_page">
        <h1>Creación de Usuario</h1>
      </div>
      <input key={id} id="file-input" type="file" accept="image/*" style={{ display: 'none' }} onChange={handleLogoChange}/>
      <button className="button_image_user" onClick={triggerFileInput}>
        <img src={currentLogo} alt="Logo" />
      </button>
      <div className="input_format">
        <input key={id} type="text" value={userName} onChange={handleUserNameChange} className="title_input_admin" placeholder="Escriba el nombre de usuario aquí"/>
      </div>
      <div className="input_format">
        <input key={id} type="text" value={password} onChange={handlePasswordChange} className="title_input_admin" placeholder="Escriba la contraseña aquí"/>
      </div>
      <div key={id} className="input_format">
        <select value={rol} onChange={handleRolChange} className="title_select_admin">
          <option value="" disabled>Seleccione rol</option>
          <option value="ADMIN">Administrador</option>
          <option value="MONITOR">Monitor</option>
        </select>
      </div>
      <button className="button_save_info_user" onClick={checkAllInformation}>Confirmar</button>
    </div>
  );
}