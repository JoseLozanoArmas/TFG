import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './BlockInternalAdminPage.css';
import logo from '../img/logo_ull.png';
import icon from '../img/icon_plus.png';

export const BlockInternalAdminPage = () => {
  const navigate = useNavigate();
  const [currentLogo, setCurrentLogo] = useState(logo);
  const [buttons, setButtons] = useState([]);

  const handleLogoChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const newLogo = URL.createObjectURL(file);
      setCurrentLogo(newLogo);
    }
  };

  const MoveToQuestionPageAdmin = () => {
    navigate('/question_admin');
  };

  const triggerFileInput = () => {
    document.getElementById("file-input").click();
  };

  const addNewButton = () => {
    if (buttons.length < 8) {
      const newButton = (
        <button key={buttons.length} className="button_new_question" onClick={MoveToQuestionPageAdmin}>
          Botón {buttons.length + 1}
        </button>
      );
      setButtons([...buttons, newButton]);
    }
  };

  const removeLastButton = () => {
    setButtons(buttons.slice(0, -1));
  };

  return (
    <div className="App_block_internal_page">
      <div className="tittle_block_internal_admin_page">
        <h1>Bloque de preguntas interior</h1>
      </div>
      <input id="file-input" type="file" accept="image/*" style={{ display: 'none' }} onChange={handleLogoChange} />
      <button className="button_logo_internal_page" onClick={triggerFileInput}>
        <img src={currentLogo} alt="Logo" />
      </button>
      {buttons}
      {buttons.length < 8 && (
        <button className="button_question" onClick={addNewButton}>
          <img src={icon} alt="Icono de pregunta" />
        </button>
      )}
      <button className="button_remove_last" onClick={removeLastButton}>
        Deshacer última pregunta
      </button>
    </div>
  );
};
