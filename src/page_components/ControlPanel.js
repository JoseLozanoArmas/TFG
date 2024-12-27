import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ControlPanel.css';

export const ControlPanel = () => {
  const navigate = useNavigate();

  const MoveToBlockGeneralAdminPage = () => {
    navigate('/block_general_admin_page');
  };

  const MoveToRanking = () => {
    navigate('/ranking');
  };

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
};
