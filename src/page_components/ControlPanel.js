import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ControlPanel.css';

const route_to_server = "http://127.0.0.1:5000/"

export const ControlPanel = () => {
  const navigate = useNavigate();
  const [isAdmin, setIsAdmin] = useState(false);
  const [isMonitor, setIsMonitor] = useState(false);

  useEffect(() => {
    const userRole = localStorage.getItem("user_role");
    setIsAdmin(userRole === "admin");
    setIsMonitor(userRole === "monitor");
  }, []);

  const MoveToBlockGeneralAdminPage = () => {
    navigate('/block_general_admin_page');
  };

  const MoveToRanking = () => {
    navigate('/ranking_internal_page'); // ESTO ANTES ESTABA CON ranking PERO LO CAMBIÉ PARA HACER PRUEBAS
  };

  const MoveToSettings = () => {
    navigate('/settings')
  };

  if (isAdmin === true) {
    return (
      <div className="control_panel_page">
        <div className="button_container">
          <span className="button_label">Ranking</span>
          <button className="button_control_panel" onClick={MoveToRanking}>
            <img src={require("../img/prize.png")} className="button_icon" alt="Ranking" />
          </button>
        </div>
  
        <div className="button_container">
          <span className="button_label">Configuración</span>
          <button className="button_control_panel" onClick={MoveToSettings}>
            <img src={require("../img/configuracion.png")} className="button_icon" alt="Configuración" />
          </button>
        </div>
  
        <div className="button_container">
          <span className="button_label">Bloque de preguntas</span>
          <button className="button_control_panel" onClick={MoveToBlockGeneralAdminPage}>
            <img src={require("../img/prueba.png")} className="button_icon" alt="Preguntas" />
          </button>
        </div>
      </div>
    );
  } else {
    return (
      <div className="control_panel_page">
        <div className="button_container">
          <span className="button_label">Ranking</span>
          <button className="button_control_panel" onClick={MoveToRanking}>
            <img src={require("../img/prize.png")} className="button_icon" alt="Ranking" />
          </button>
        </div>
  
        <div className="button_container">
          <span className="button_label">Bloque de preguntas</span>
          <button className="button_control_panel" onClick={MoveToBlockGeneralAdminPage}>
            <img src={require("../img/prueba.png")} className="button_icon" alt="Preguntas" />
          </button>
        </div>
      </div>
    );
  }

  
};
