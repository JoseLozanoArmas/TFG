import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './BlockInternalAdminPage.css';
import logo from '../img/logo_ull.png';
import icon from '../img/icon_plus.png';

const route_to_server = "http://127.0.0.1:5000/"

export const BlockInternalAdminPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  const current_block_name = id;

  const [currentLogo, setCurrentLogo] = useState(() => {
    const savedLogo = localStorage.getItem(`logo_${id}`);
    if (savedLogo) {
      return JSON.parse(savedLogo);
    } else {
      return logo;
    }
  });

  useEffect(() => {
    if (!current_block_name) {
      return;
    }
    const getInfoQuestionButtons = async() => {
      try { // Llamamos al método que crea la carpeta del bloque del usuario
        const response = await fetch(route_to_server + 'get-questions-of-internal-block', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: current_block_name[current_block_name.length - 1]
          }),
        });
        const data = await response.json();
        if (response.ok) {
          setButtons(JSON.parse(data.data));
        } else {
          if (response.status !== 500) {
            alert(`Error: ${data.message}`);
          }
        }
      } catch (error) {
        alert('Error al conectar con el servidor.');
        console.error(error);
      }
    }
    getInfoQuestionButtons();
  },[current_block_name])

  const [buttons, setButtons] = useState([])

  /*
  const [buttons, setButtons] = useState(() => {
    const savedButtons = localStorage.getItem(`button_${id}`);
    if (savedButtons) {
      return JSON.parse(savedButtons);
    } else {
      return [];
    }
  });
  */

  const [isAdmin, setIsAdmin] = useState(false);
  const [isMonitor, setIsMonitor] = useState(false);
  const [isTemporalyUser, setIsTemporalyUser] = useState(false);
  const [userName, setName] = useState("");
  const [saveRol, setSaveRol] = useState("");

  useEffect(() => {
    const userRole = localStorage.getItem("user_role");
    setIsAdmin(userRole === "admin");
    setIsMonitor(userRole === "monitor");
    const getUserName = localStorage.getItem("name_user");
    setName(getUserName);
    setSaveRol(userRole);
  }, []);

  const handleLogoChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const newLogo = URL.createObjectURL(file);
      setCurrentLogo(newLogo);
    }
  };

  const MoveToQuestionPageAdmin = async (id) => {
    if ((isAdmin === false) && (isMonitor === false)) {
      let block_name = current_block_name[current_block_name.length - 1]
      block_name = String(block_name)
      try { // Llamamos al método que crea la carpeta del bloque del usuario
        const response = await fetch(route_to_server + 'create-question-folder-user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: userName,
            block_name: block_name, 
            question_name: id
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
    navigate(`/${id}`);
  };

  const triggerFileInput = () => {
    document.getElementById("file-input").click();
  };

  const addNewButton = async () => {
    if (buttons.length < 8) {
      // ANTES EN NAME ESTABA question_${buttons.length + 1} LO DE AHORA ES UN EXPERIMENTO
      let new_question_name = current_block_name + `_question_${buttons.length + 1}`
      const newButton = {
        id: buttons.length + 1,
        label: `Pregunta ${buttons.length + 1}`,
        name: new_question_name,
      };

      localStorage.setItem("current_question_name", newButton.name);

      setButtons((prevButtons) => [...prevButtons, newButton]);
      try {
        const response = await fetch(route_to_server + 'create-question-block-folder-admin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: current_block_name,
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

      try {
        const response = await fetch(route_to_server + 'regist-question-button', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: current_block_name[current_block_name.length - 1],
            question_id: newButton.id,
            label: newButton.label, 
            name: newButton.name,
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
    let question_id = buttons[buttons.length - 1].id
    setButtons((prevButtons) => prevButtons.slice(0,-1));
    try {
      const response = await fetch(route_to_server + 'delete-question-folder-admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: current_block_name,
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

    try {
      const response = await fetch(route_to_server + 'delete-question-button-json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: current_block_name[current_block_name.length - 1],
          question_id: question_id, 
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

    try { // Borramos de data_information_app la pregunta
      const response = await fetch(route_to_server + 'delete-question-regist-admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: current_block_name[current_block_name.length - 1],
          question_id: question_id
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
      } else {
        if (response.status !== 500) {
          alert(`Error: ${data.message}`);
        }
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error); 
    }

  };

  useEffect(() => {
    localStorage.setItem(`logo_${id}`, JSON.stringify(currentLogo));
  }, [currentLogo]);


  const ChangePermission = () => {
    if (isTemporalyUser === false) {
      if (isAdmin === true) { setIsAdmin(false) }
      if (isMonitor === true) { setIsMonitor(false) }
      setIsTemporalyUser(true) 
      alert("Permisos cambiados a usuario")
    } else {
      setIsTemporalyUser(false);
      if (saveRol === "admin") { 
        setIsAdmin(true)
        alert("Permisos de administrador recuperados") 
      }
      if (saveRol === "monitor") { 
        setIsMonitor(true) 
        alert("Permisos de monitor recuperados")
      }
    }
  }

  const MoveToPreviousPage = () => {
    navigate('/block_general_admin_page');
  };

  const MakeCorrection = async () => {
    try {
      const response = await fetch(route_to_server + 'check_is_possible_to_correct', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: userName,
          block_id: current_block_name,
        }),
      });
      const data = await response.json();
      if (data.data === true) {

        const regist = await fetch(route_to_server + 'regist-final-time', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: userName,
            block_id: current_block_name,
          }),
        });

        const response = await fetch(route_to_server + 'calculate-puntuation-for-user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: userName,
            block_id: current_block_name,
          }),
        });
      } else {
        alert("No se han enviado todas las respuestas")
        return;
      }
    } catch (error) {
      console.error('Error al intentar corregir', error);
      return false;
    }

    alert("Corrección realizada con éxito. Cuestionario completado!!!")
    navigate(`/ranking_internal_page/${current_block_name}`)
  }
  
  if ((isAdmin === true) || (isMonitor === true)) {
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
        {buttons.length < 8 && (
          <button className="button_question" onClick={addNewButton}>
            <img src={icon} alt="Icono de pregunta" />
          </button>
        )}
        {buttons.length >= 1 && (
          <button className="button_remove_last" onClick={removeLastButton}>
            Deshacer última pregunta
          </button>
        )}
        {buttons.length >= 1 && (
          <button className="button_change_to_admin_or_monitor" onClick={ChangePermission}>
            Probar cómo usuario
          </button>
        )}
        <button className="button_move_previous_page" onClick={MoveToPreviousPage}>
            Volver a la página anterior
        </button>
      </div>
    );
  } else if(isTemporalyUser === true) {
    return (
      <div className="App_block_internal_page">
        <div className="tittle_block_internal_admin_page">
          <h1>Bloque de preguntas interior</h1>
        </div>
        <img src={currentLogo} alt="Logo" />
        {buttons.map((button) => ( 
          <button key={button.id} className="button_new_question" onClick={() => {MoveToQuestionPageAdmin(button.name);}}>
            {button.label}
          </button>
        ))}
        <button className="button_change_to_admin_or_monitor_activated" onClick={ChangePermission}>
          Volver al rol anterior
        </button>
        <button className="button_move_previous_page" onClick={MoveToPreviousPage}>
            Volver a la página anterior
        </button>
      </div>
    );
  } else {
      return (
        <div className="App_block_internal_page">
          <div className="tittle_block_internal_admin_page">
            <h1>Bloque de preguntas interior</h1>
          </div>
          <img src={currentLogo} alt="Logo" />
          {buttons.map((button) => ( 
            <button key={button.id} className="button_new_question" onClick={() => {MoveToQuestionPageAdmin(button.name);}}>
              {button.label}
            </button>
          ))}
          <button className="button_correct_code" onClick={() => MakeCorrection()}>Finalizar intento</button>
          <button className="button_move_previous_page" onClick={MoveToPreviousPage}>
            Volver a la página anterior
          </button>
        </div>
      );
  }
};
