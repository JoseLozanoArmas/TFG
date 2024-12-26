import React, { useState } from 'react';
import './QuestionPageAdmin.css';

export const QuestionPageAdmin = () => {
  const [title, setTitle] = useState(); 
  const [description, setDescription] = useState();
  const [puntuation, setPuntuation] = useState(0);

  const handleTitleChange = (event) => {
    setTitle(event.target.value); 
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handlePuntuationChange = (event) => {
    setPuntuation(event.target.value);
  }

  return (
    <div className="App_question_page_admin">
      <div className="tittle_question_page_admin">
        <input type="text" value={title} onChange={handleTitleChange} className="title_input_admin" placeholder="Escriba el título aquí"/>
      </div>
      <div className="description_question_page_admin">
        <input type="text" value={description} onChange={handleDescriptionChange} className="description_input_admin" placeholder="Escriba la descripción aquí"/>
      </div>
      <div className="puntuation_question_page_admin">
        <input type="text" value={puntuation} onChange={handlePuntuationChange} className="puntuation_input_admin"/>
      </div>
      <div>Pruebas</div>
      <button>Guardar</button>
    </div>
  );
};
