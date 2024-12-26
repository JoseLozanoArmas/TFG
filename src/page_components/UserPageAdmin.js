import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './UserPageAdmin.css';

export const UserPageAdmin = () => {
  const USER_NAME = "admin";
  const PASSWORD = "1234";
  const navigate = useNavigate();

  const GoToGeneralAdminPage = () => {
    navigate('/block_general_admin_page'); 
  };

  const GoToUserPage = () => {
    navigate('/');
  };

  const [user_name, setTexto] = useState('');
  const [user_password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const SaveUser = async () => {
    if (!user_name.trim()) { 
      alert('Por favor introduzca un nombre de usuario.');
      return;
    }

    if (!user_password.trim()) {
      alert('Por favor introduzca una contraseña');
      return;  
    }

    if ((user_name === USER_NAME) && (user_password === PASSWORD)) {
      alert('Contraseña aceptada');
      GoToGeneralAdminPage();
    } else {
        alert('Usuario o contraseña incorrectos');
        return;
    }
  };

    return (
      <div className="App">
        <header className="App-header">
          <img src={require('../img/user_img.png')} alt="User" className="user-image" />
            {"Login"}
            <div className="input-box">
              <textarea className="textarea_user_page_admin_username" value={user_name} onChange={(e) => setTexto(e.target.value)} placeholder="Inserte nombre de usuario..."></textarea>
              <input type="password" className='textarea_user_page_admin_password' value={user_password} onChange={(e) => setPassword(e.target.value)} placeholder="Inserte contraseña..."/>
              <button onClick={SaveUser}>Iniciar</button>
              <button class="admin_button" onClick={GoToUserPage}>¿Entrar cómo usuario?</button>
            </div>
        </header>
    </div>
  );
};
