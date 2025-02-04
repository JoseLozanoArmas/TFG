import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './InternalUserPage.css';
import default_user_image from '../img/user_img.png';

const route_to_server = "http://127.0.0.1:5000/"

export const InternalUserPage = () => {
  const navigate = useNavigate();
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

  const [userName, setUserName] = useState(() => {
    const savedUserName = localStorage.getItem("userName");
    if (savedUserName) {
      return JSON.parse(savedUserName);
    } else {
      return "";
    }
  }); 

  const [password, setPassword] = useState(() => {
    const savedPassword = localStorage.getItem("password");
    if (savedPassword) {
      return JSON.parse(savedPassword);
    } else {
      return "";
    }
  }); 

  const [rol, setRol] = useState(() => {
    const savedRol = localStorage.getItem("rol");
    if (savedRol) {
      return JSON.parse(savedRol);
    } else {
      return "";
    }
  }); 

  const [isAdmin, setIsAdmin] = useState(false);


  useEffect(() => {
    const userRole = localStorage.getItem('user_role');
    setIsAdmin(userRole === 'admin');
  }, []);

  useEffect(() => {
    localStorage.setItem("userName", JSON.stringify(userName));
    localStorage.setItem("password", JSON.stringify(password));
    localStorage.setItem("rol", JSON.stringify(rol));
  })

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

  const checkAllInformation = async () => {
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

    let new_user = userName + "," + password + "," + rol;
    try {
      const response = await fetch(route_to_server + 'add-new-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: new_user
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);

        // METER CONDICIÓN PARA VOLVER A LA PAGINA ANTERIOR

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
      <input id="file-input" type="file" accept="image/*" style={{ display: 'none' }} onChange={handleLogoChange}/>
      <button className="button_image_user" onClick={triggerFileInput}>
        <img src={currentLogo} alt="Logo" />
      </button>
      <div className="input_format">
        <input type="text" value={userName} onChange={handleUserNameChange} className="title_input_admin" placeholder="Escriba el nombre de usuario aquí"/>
      </div>
      <div className="input_format">
        <input type="text" value={password} onChange={handlePasswordChange} className="title_input_admin" placeholder="Escriba la contraseña aquí"/>
      </div>
      <div className="input_format">
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