import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './QuestionPageAdmin.css';
import icon from '../img/icon_plus.png';

export const QuestionPageAdmin = () => {
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
  const [first_puntuation, setFirstPuntuation] = useState(0);
  const [second_puntuation, setSecondPuntuation] = useState(0);
  const [third_puntuation, setThirdPuntuation] = useState(0);
  const [uploadedFiles, setUploadedFiles] = useState({ file1: null, file2: null, file3: null, fileUser: null});
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

  const handleFirstPuntuationChange = (event) => {
    setFirstPuntuation(event.target.value);
  }

  const handleSecondPuntuationChange = (event) => {
    setSecondPuntuation(event.target.value);
  }

  const handleThirdPuntuationChange = (event) => {
    setThirdPuntuation(event.target.value);
  }

  const handleFileUpload = (event, key) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFiles((prev) => ({ ...prev, [key]: file.name }));
    }
  };

  const triggerFileInput = (id) => {
    document.getElementById(id).click();
  };

  const triggerFileInputUser = (id) => {
    document.getElementById(id).click();
  }

  const addNewButton = () => {
    const newButton = {
      id: buttons.length + 1,
      label: `Pregunta ${buttons.length + 1}`
    };
    setButtons((prevButtons) => [...prevButtons, newButton]);
  };

  const checkAllInformation = () => {
    if (!title.trim()) { 
      alert("Por favor introduzca un titulo a la pregunta");
      return;
    }

    if (!description.trim()) { 
      alert("Por favor introduzca una descripción a la pregunta");
      return;
    }

    if (first_puntuation <= 0) {
      alert("Por favor introduzca una puntuación mayor a 0 a la primera prueba");
      return;
    }

    if (uploadedFiles.file1 == null) {
      alert("No se ha subido la prueba 1");
      return;
    }

    if (second_puntuation <= 0) {
      alert("Por favor introduzca una puntuación mayor a 0 a la primera prueba");
      return;
    }

    if (uploadedFiles.file2 == null) {
      alert("No se ha subido la prueba 2");
      return;
    }

    if (third_puntuation <= 0) {
      alert("Por favor introduzca una puntuación mayor a 0 a la primera prueba");
      return;
    }

    if (uploadedFiles.file3 == null) {
      alert("No se ha subido la prueba 3");
      return;
    }

    alert("añadir la condición para que cuando se pulse el boton de confirmar te mande a la pagina de las preguntas")
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
        // METER LA CONDICIÓN PARA VOLVER A LA PÁGINA ANTERIOR
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
        <div className="puntuation_question_page_admin">
          <button className="button_submit_test" onClick={() => triggerFileInput('fileInput1')}>{content_of_button_admin}</button>
          <input id="fileInput1" type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, 'file1')} />
          {uploadedFiles.file1 && <span className="file_name_display">{uploadedFiles.file1}</span>}
          <div className="label_puntuation_admin">Añada una puntuación al final de la pregunta:</div>
          <input type="text" value={first_puntuation} onChange={handleFirstPuntuationChange} className="puntuation_input_admin"/>
        </div>
        <button className="button_question" onClick={addNewButton}>
          <img src={icon} alt="Icono de pregunta" />
        </button>
        <button className="button_save_question_page_admin" onClick={checkAllInformation}>Confirmar</button>
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
