import React from 'react';
import './BlockInternalAdminPage.css';
import logo from '../img/logo_ull.png';

export const BlockInternalAdminPage = () => {
  return (
    <div className="App_block_internal_page">
      <div className="tittle_block_internal_admin_page">
        <h1>Bloque de preguntas interior</h1>
      </div>
      <button className="button_logo_internal_page">
        <img src={logo} />
      </button>
    </div>
  );
}