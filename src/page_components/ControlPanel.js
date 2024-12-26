import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ControlPanel.css';

export const ControlPanel = () => {
  const navigate = useNavigate();

  const MoveToBlockGeneralAdminPage = () => {
    navigate('/block_general_admin_page');
  };

  const MoveToRanking = () => {
    alert("pendiente")
  };

  return (
    <div className="control_panel_page">
      <button className="button_control_panel" onClick={MoveToRanking}>Ranking</button>
      <button className="button_control_panel" onClick={MoveToBlockGeneralAdminPage}>Preguntas</button>
    </div>
  );
}