import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './BlockInternalAdminPage.css';
import logo from '../img/logo_ull.png';
import icon from '../img/icon_plus.png';

export const BlockInternalAdminPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [currentLogo, setCurrentLogo] = useState(() => {
    const savedLogo = localStorage.getItem(`logo_${id}`);
    if (savedLogo) {
      return JSON.parse(savedLogo);
    } else {
      return logo;
    }
  });
  const [buttons, setButtons] = useState(() => {
    const savedButtons = localStorage.getItem(`button_${id}`);
    if (savedButtons) {
      return JSON.parse(savedButtons);
    } else {
      return [];
    }
  });

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
      const newButton = {
        id: buttons.length + 1,
        label: `Pregunta ${buttons.length + 1}`
      };
      setButtons((prevButtons) => [...prevButtons, newButton]);
    }
  };

  const removeLastButton = () => {
    setButtons((prevButtons) => prevButtons.slice(0,-1));
  };

  useEffect(() => {
    localStorage.setItem(`logo_${id}`, JSON.stringify(currentLogo));
    localStorage.setItem(`button_${id}`, JSON.stringify(buttons));
  }, [currentLogo, buttons]);

  return (
    <div className="App_block_internal_page">
      <div className="tittle_block_internal_admin_page">
        <h1>Bloque de preguntas interior</h1>
      </div>
      <input id="file-input" type="file" accept="image/*" style={{ display: 'none' }} onChange={handleLogoChange} />
      <button className="button_logo_internal_page" onClick={triggerFileInput}>
        <img src={currentLogo} alt="Logo" />
      </button>
      {buttons.map((button) => (
        <button key={button.id} className="button_new_question" onClick={MoveToQuestionPageAdmin}>
          {button.label}
        </button>
      ))}
      {buttons.length < 8 && (
        <button className="button_question" onClick={addNewButton}>
          <img src={icon} alt="Icono de pregunta" />
        </button>
      )}
      {buttons.length >= 0 && (
        <button className="button_remove_last" onClick={removeLastButton}>
          Deshacer última pregunta
        </button>
      )}
    </div>
  );
};
