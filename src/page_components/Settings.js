import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Settings.css';

export const Settings = () => {
  const navigate = useNavigate();

  const MoveToDeleteOptions = () => {
    navigate('/delete_options');
  };

  const MoveToUsers = () => {
    navigate('/general_users');
  };

  return (
    <div className="settings_page">
      <div className="button_container">
        <span className="button_label">Usuarios</span>
        <button className="button_settings" onClick={MoveToUsers}>
          <img src={require("../img/usuarios.png")} className="button_icon" alt="Users" />
        </button>
      </div>
      <div className="button_container">
        <span className="button_label">Opciones de borrado</span>
        <button className="button_settings" onClick={MoveToDeleteOptions}>
          <img src={require("../img/configuracion.png")} className="button_icon" alt="Delete options" />
        </button>
      </div>
    </div>
  );
};
