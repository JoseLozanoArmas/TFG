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

  const MoveToQuestionPageAdmin = async (id) => {
    navigate(`/${id}`);
  };

  const triggerFileInput = () => {
    document.getElementById("file-input").click();
  };

  const [isAdmin, setIsAdmin] = useState(false);
  const [isMonitor, setIsMonitor] = useState(false);
  const [currentBlockName, setCurrentBlockName] = useState("");

  useEffect(() => {
    const userRole = localStorage.getItem("user_role");
    setIsAdmin(userRole === "admin");
    setIsMonitor(userRole === "monitor");
    const getName = localStorage.getItem("current_block_name");
    setCurrentBlockName(getName);
  }, []);

  const addNewButton = async () => {
    if (buttons.length < 8) {
      const newButton = {
        id: buttons.length + 1,
        label: `Pregunta ${buttons.length + 1}`,
        name: `question_${buttons.length + 1}`
      };

      localStorage.setItem("current_question_name", newButton.name);

      setButtons((prevButtons) => [...prevButtons, newButton]);
      try {
        const response = await fetch('http://127.0.0.1:5000/create-question-block-folder-admin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: currentBlockName,
            question_name: newButton.name, 
          }),
        });
    
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (error) {
        alert('Error al conectar con el servidor.');
        console.error(error);
      }
    }
  };

  const removeLastButton = async () => {
    let name_question_folder = buttons[buttons.length - 1].name
    setButtons((prevButtons) => prevButtons.slice(0,-1));
    try {
      const response = await fetch('http://127.0.0.1:5000/delete-question-folder-admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: currentBlockName,
          question_name: name_question_folder, 
        }),
      });
  
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }
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
        <button key={button.id} className="button_new_question" onClick={() => {MoveToQuestionPageAdmin(button.name);}}>
          {button.label}
        </button>
      ))}
      {buttons.length < 8 && ((isAdmin === true) || (isMonitor === true)) && (
        <button className="button_question" onClick={addNewButton}>
          <img src={icon} alt="Icono de pregunta" />
        </button>
      )}
      {buttons.length >= 0 && ((isAdmin === true) || (isMonitor === true)) && (
        <button className="button_remove_last" onClick={removeLastButton}>
          Deshacer última pregunta
        </button>
      )}
    </div>
  );
};
