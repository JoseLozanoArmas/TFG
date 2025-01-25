import React, { useState, useEffect } from 'react';
import { Navigate, Route, useNavigate, useParams } from 'react-router-dom';
import './QuestionPageAdmin.css';
import icon from '../img/icon_plus.png';

export const QuestionPageAdmin = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [title, setTitle] = useState(() => {
    const savedTittle = localStorage.getItem("title");
    if (savedTittle) {
      return JSON.parse(savedTittle);
    } else {
      return [];
    }
  }); 
  const [description, setDescription] = useState(() => {
    const savedDescription = localStorage.getItem("description");
    if (savedDescription) {
      return JSON.parse(savedDescription);
    } else {
      return [];
    }
  });
  const [uploadedFiles, setUploadedFiles] = useState({});
  const [block_name, setBlockName] = useState("");
  const [question_name, setQuestionName] = useState("");
  const make_invisible = { display: "none" }
  const content_of_button_admin = "Suba una prueba";
  const content_of_button_user = "Suba su código";

  const [buttons, setButtons] = useState(() => {
    const savedButtons = localStorage.getItem(`button_${id}`);
    if (savedButtons) {
      return JSON.parse(savedButtons);
    } else {
      return [];
    }
  });

  const [isAdmin, setIsAdmin] = useState(false);
  const [isMonitor, setIsMonitor] = useState(false);
  const [userName, setName] = useState("");

  useEffect(() => {
    const userRole = localStorage.getItem("user_role");
    setIsAdmin(userRole === "admin");
    setIsMonitor(userRole === "monitor")
    const getName = localStorage.getItem("name_user");
    setName(getName);
    const getBlockName = localStorage.getItem("current_block_name")
    setBlockName(getBlockName);
    const getQuestionName = localStorage.getItem("current_question_name")
    setQuestionName(getQuestionName)
  }, []);

  useEffect(() => {
    localStorage.setItem("title", JSON.stringify(title));
    localStorage.setItem("description", JSON.stringify(description));
  })

  const handleTitleChange = (event) => {
    setTitle(event.target.value); 
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handlePuntuationChange = (event, key) => {
    const value = event.target.value;
    setButtons((prevButtons) =>
      prevButtons.map((button) =>
        button.id === key ? { ...button, puntuation: value } : button
      )
    );
  }

  const handleFileUpload = (event, key) => {
    const file = event.target.files[0];
    let save_name = file.name;
    setButtons((prevButtons) =>
      prevButtons.map((button) =>
        button.id === key ? { ...button, file: save_name || null} : button
      )
    );
  };

  const triggerFileInputUser = (id) => {
    document.getElementById(id).click();
  }

  const addNewButton = async () => {
    const newButton = {
      id: buttons.length + 1,
      name: `prueba_${buttons.length + 1}`,
      file: null,
      puntuation: 0
    };
    setButtons((prevButtons) => [...prevButtons, newButton]);
  };

  const removeCurrentButton = async (id) => {
    setButtons((prevButtons) => prevButtons.filter((button) => button.id !== id));
  }

  const removeAll = async (id) => {
    setButtons((prevButtons) => []);
  }

  const checkAllInformation = () => {
    if (!title.trim()) { 
      alert("Por favor introduzca un titulo a la pregunta");
      return;
    }

    if (!description.trim()) { 
      alert("Por favor introduzca una descripción a la pregunta");
      return;
    }

    // Comprobamos que todos los botones tengan puntuación y pruebas añadidas
    let is_possible_to_send_files = true;
    {buttons.forEach((button) => {
      if (button.file === null) {
        alert(`En la prueba ${button.id} no se introdujo ningún fichero de prueba`);
        is_possible_to_send_files = false;
      }
      if (button.puntuation <= 0) {
        alert(`En la prueba ${button.id} no se introdujo una puntuación mayor a 0`);
        is_possible_to_send_files = false;
      }
    })}

    if (is_possible_to_send_files === true) {

      /*
      let previous_route = "block_internal_admin_page/" + block_name
      alert("Información registrada con éxito")
      navigate(`/${previous_route}`)
      */
      alert("descomentar lo de moverme a la página anterior")
    } else {
      return;
    }
  };

  const SendFileUser = async () => {
    if (uploadedFiles.fileUser === null) {
      alert("Error. No se ha subido ninguna entrada")
      return;
    }

    const fileInput = document.getElementById('fileInputUser').files[0];
    const formData = new FormData();
    formData.append('file', fileInput); // Agregar archivo
    formData.append('userNameData', userName); // Agregar nombre de usuario

    try {
      const response = await fetch('http://127.0.0.1:5000/upload-file-user', {
        method: 'POST',
        body: formData,
        userNameData: JSON.stringify({ text: userName }),
      });
  
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        let previous_route = "block_internal_admin_page/" + block_name
        navigate(`/${previous_route}`)
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }
  }
  
  if ((isAdmin === true) || (isMonitor === true)) {
    return (
      <div className="App_question_page_admin">
        <div className="tittle_question_page_admin">
          <input type="text" value={title} onChange={handleTitleChange} className="title_input_admin" placeholder="Escriba el título aquí"/>
        </div>
        <div className="description_question_page_admin">
          <input type="text" value={description} onChange={handleDescriptionChange} className="description_input_admin" placeholder="Escriba la descripción aquí"/>
        </div>
        {buttons.map((button) => (
        <div key={button.id} className="puntuation_question_page_admin">
          <button className="button_submit_test" onClick={() => document.getElementById(`fileInput_${button.id}`).click()}>{content_of_button_admin}</button>
          <input id={`fileInput_${button.id}`} type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, button.id)} />
          {button.file && <span className="file_name_display">{button.file}</span>}
          <div className="label_puntuation_admin">Añada una puntuación al final de la pregunta:</div>
          <input type="number" value={button.puntuation} onChange={(e) => handlePuntuationChange(e, button.id)} className="puntuation_input_admin"/>
          <button className="button_delete_test" onClick={() => removeCurrentButton(button.id)}>
            Eliminar prueba
          </button>
        </div>
        ))}
        <button className="button_question" onClick={addNewButton}>
          <img src={icon} alt="Icono de pregunta" />
        </button>
        {buttons.length >= 1 && (
          <button className="button_save_question_page_admin" onClick={checkAllInformation}>Confirmar</button>
        )}
      </div>
    );
  } else {
    return (
      <div className="App_question_page_user">
        <div className="tittle_question_page_admin">
          <input type="text" value={title} className="title_input_admin" readOnly/>
        </div>
        <div className="description_question_page_admin">
          <input type="text" value={description} className="description_input_admin" readOnly/>
        </div>
        <div className="user_submit_code">
          <button className="button_submit_code" onClick={() => triggerFileInputUser('fileInputUser')}>{content_of_button_user}</button>
          <input id="fileInputUser" type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, 'fileUser')} />
          {uploadedFiles.fileUser && <span className="file_name_display">{uploadedFiles.fileUser}</span>}
        </div>
        <div className="user_submit_code">
          <button className="button_submit_code" onClick={SendFileUser}>Confirmar</button>
        </div>
      </div>
    )
  }
};
