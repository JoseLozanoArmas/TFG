import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './UserPageAdmin.css';

export const UserPageAdmin = () => {
    const USER_NAME = "admin"
    const PASSWORD = "1234"
    const navigate = useNavigate();

    const GoToUser = () => {
        navigate('/'); 
    };

    const [user_name, setTexto] = useState('');
    const [user_password, setPassword] = useState('');

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
            GoToUser();
        } else {
            alert('Usuario o contraseña incorrectos');
            return;
        }
    };

    return (
        <div className="App">
          <header className="App-header">
            <img src={require('../img/user_img.png')} alt="User" className="user-image" />
            {"Admin"}
            <div className="input-box">
              <textarea className='textarea_user_page_admin_username' value={user_name} onChange={(e) => setTexto(e.target.value)} placeholder="Inserte nombre de usuario..."></textarea>
              <textarea className='textarea_user_page_admin_password' value={user_password} onChange={(e) => setPassword(e.target.value)} placeholder="Inserte contraseña..."></textarea>
              <button onClick={SaveUser}>Iniciar</button>
            </div>
          </header>
        </div>
      );
}

