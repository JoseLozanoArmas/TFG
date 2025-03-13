import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserPageAdmin.css';
import { route_to_server } from '../App';

export const UserPageAdmin = () => {
  const navigate = useNavigate();

  const [user_name, setTexto] = useState('');
  const [user_password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const [saveJson, setSaveJson] = useState();

  useEffect(() => {
    const getJsonData = async () => {
      try {
        const response = await fetch(route_to_server + 'get-info-users-json'); // Recibimos los usuarios registrados
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
  

  const GoToControlPanel = () => {
    navigate('/control_panel'); 
  };

  const GoToUserPage = () => {
    navigate('/');
  };

  const togglePasswordVisibility = () => { // Gestionamos la visibilidad de la contraseña
    setShowPassword(!showPassword);
  };

  const comprobate_user = (user, password) => { // Comprobamos los permisos de usuario
    for (let i = 0; i < saveJson.length; ++i) {
      if ((user === saveJson[i].username) && (password === saveJson[i].password)) {
        if (saveJson[i].rol === "ADMIN") { localStorage.setItem("user_role","admin"); }
        if (saveJson[i].rol === "MONITOR") { localStorage.setItem("user_role","monitor"); }
        return true;
      }
    }
    return false;
  }

  const SaveUser = async () => { // Comprobamos el registro de usuario
    if (!user_name.trim()) { 
      alert('Por favor introduzca un nombre de usuario.');
      return;
    }

    if (!user_password.trim()) {
      alert('Por favor introduzca una contraseña');
      return;  
    }

    if (comprobate_user(user_name, user_password)) {
      alert("Contraseña aceptada");
      GoToControlPanel();
    } else {
      alert("Usuario o contraseña incorrectos");
      setPassword("");
      return;
    }
  };

    return (
      <div className="App">
        <header className="App-header">
          <img src={require("../img/user_img.png")} className="user-image" alt=""/>
            {"Login"}
            <div className="input-box">
              <textarea className="textarea_user_page_admin_username" value={user_name} onChange={(e) => setTexto(e.target.value)} placeholder="Inserte nombre de usuario..."></textarea>
              <div className="password-container">
                <input type={showPassword ? "text" : "password"} className="textarea_user_page_admin_password" value={user_password} onChange={(e) => setPassword(e.target.value)} placeholder="Inserte contraseña..."/>
                <button onClick={togglePasswordVisibility} className="visibility-button">
                  <img src={showPassword ? require("../img/eye.png") : require("../img/closed_eye.png")} className ="visibility-image" alt=""/>
                </button>
              </div>
              <button onClick={SaveUser}>Iniciar</button>
              <button className="admin_button" onClick={GoToUserPage}>¿Entrar cómo usuario?</button>
            </div>
        </header>
    </div>
  );
};
