import React, { useState } from 'react';
import './QuestionPageAdmin.css';

export const QuestionPageAdmin = () => {
  const [title, setTitle] = useState(""); 
  const [description, setDescription] = useState("");
  const [first_puntuation, setFirstPuntuation] = useState(0);
  const [second_puntuation, setSecondPuntuation] = useState(0);
  const [third_puntuation, setThirdPuntuation] = useState(0);
  const [uploadedFiles, setUploadedFiles] = useState({ file1: null, file2: null, file3: null });
  const make_invisible = { display: "none" }
  const content_of_button = "Suba una prueba"

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

  return (
    <div className="App_question_page_admin">
      <div className="tittle_question_page_admin">
        <input type="text" value={title} onChange={handleTitleChange} className="title_input_admin" placeholder="Escriba el título aquí"/>
      </div>
      <div className="description_question_page_admin">
        <input type="text" value={description} onChange={handleDescriptionChange} className="description_input_admin" placeholder="Escriba la descripción aquí"/>
      </div>
      <div className="puntuation_question_page_admin">
        <button className="button_submit_test" onClick={() => triggerFileInput('fileInput1')}>{content_of_button}</button>
        <input id="fileInput1" type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, 'file1')} />
        {uploadedFiles.file1 && <span className="file_name_display">{uploadedFiles.file1}</span>}
        <div className="label_puntuation_admin">Añada una puntuación al final de la pregunta:</div>
        <input type="text" value={first_puntuation} onChange={handleFirstPuntuationChange} className="puntuation_input_admin"/>
      </div>
      <div className="puntuation_question_page_admin">
        <button className="button_submit_test" onClick={() => triggerFileInput('fileInput2')}>{content_of_button}</button>
        <input id="fileInput2" type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, 'file2')} />
        {uploadedFiles.file2 && <span className="file_name_display">{uploadedFiles.file2}</span>}
        <div className="label_puntuation_admin">Añada una puntuación al final de la pregunta:</div>
        <input type="text" value={second_puntuation} onChange={handleSecondPuntuationChange} className="puntuation_input_admin"/>
      </div>
      <div className="puntuation_question_page_admin">
        <button className="button_submit_test" onClick={() => triggerFileInput('fileInput3')}>{content_of_button}</button>
        <input id="fileInput3" type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, 'file3')} />
        {uploadedFiles.file3 && <span className="file_name_display">{uploadedFiles.file3}</span>}
        <div className="label_puntuation_admin">Añada una puntuación al final de la pregunta:</div>
        <input type="text" value={third_puntuation} onChange={handleThirdPuntuationChange} className="puntuation_input_admin"/>
      </div>
      <button className="button_save_question_page_admin" onClick={checkAllInformation}>Confirmar</button>
    </div>
  );
};
