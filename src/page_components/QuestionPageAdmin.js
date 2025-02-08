import React, { useState, useEffect } from 'react';
import { Navigate, Route, useNavigate, useParams } from 'react-router-dom';
import './QuestionPageAdmin.css';
import icon from '../img/icon_plus.png';

const route_to_server = "http://127.0.0.1:5000/"

export const QuestionPageAdmin = () => {
  // localStorage.clear();
  const navigate = useNavigate();
  const { id } = useParams();

  const separate = id.split("_");
  const block = separate.slice(0, 2).join("_"); // Guardar el nombre del bloque

  const [title, setTitle] = useState(() => {
    const savedTittle = localStorage.getItem(`title_${id}`);
    if (savedTittle) {
      return JSON.parse(savedTittle);
    } else {
      return [];
    }
  }); 
  const [description, setDescription] = useState(() => {
    const savedDescription = localStorage.getItem(`description_${id}`);
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
  const content_of_button_admin_enter_file = "Suba una entrada";
  const content_of_button_admin_result_file = "Suba el resultado esperado";
  const content_of_button_user = "Suba su código";
  let activate_function_update = false

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
  const [isTemporalyUser, setIsTemporalyUser] = useState(false);
  const [saveRol, setSaveRol] = useState("");


  useEffect(() => {
    const userRole = localStorage.getItem("user_role");
    setIsAdmin(userRole === "admin");
    setIsMonitor(userRole === "monitor")
    const getName = localStorage.getItem("name_user");
    setName(getName);
    setBlockName(block);
    setQuestionName(id)
    setSaveRol(userRole);
  }, []);

  useEffect(() => {
    localStorage.setItem(`title_${id}`, JSON.stringify(title));
    localStorage.setItem(`description_${id}`, JSON.stringify(description));
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
    if (key === "fileUser") {
      setUploadedFiles((lastFiles) => ({ ...lastFiles, fileUser: file.name }));
    } else {
      setButtons((prevButtons) =>
        prevButtons.map((button) =>
          button.id === key ? { ...button, file: file.name } : button
        )
      );
    }
  };

  const handleResultFileUpload = (event, key) => {
    const file = event.target.files[0];
    if (key === "fileUser") {
      setUploadedFiles((lastFiles) => ({ ...lastFiles, fileUser: file.name }));
    } else {
      setButtons((prevButtons) =>
        prevButtons.map((button) =>
          button.id === key ? { ...button, result_file: file.name } : button
        )
      );
    }
  };

  const triggerFileInputUser = (id) => {
    document.getElementById(id).click();
  }

  const addNewButton = async () => {
    const newButton = {
      id: buttons.length + 1,
      name: `prueba_${buttons.length + 1}`,
      file: null,
      result_file: null,
      puntuation: 0
    };
    setButtons((prevButtons) => [...prevButtons, newButton]);
  };

  const removeCurrentButton = async (id) => {
    const buttonToRemove = buttons.find((button) => button.id === id);
    let save_enter_test_name = buttonToRemove.file;
    let save_result_test_name = buttonToRemove.result_file;
    if (buttonToRemove.file !== null) {     
      try { // Guardamos la info de la pregunta en el JSON de registro
        const response = await fetch(route_to_server + 'delete-selected-test', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: block_name,
            question_name: question_name, 
            enter_test_name: save_enter_test_name,
            result_test_name: save_result_test_name
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
    setButtons((prevButtons) => prevButtons.filter((button) => button.id !== id));
  }

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

  const checkAllInformation = async () => {
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
        alert(`En la prueba ${button.id} no se introdujo ningún fichero de entrada`);
        is_possible_to_send_files = false;
      }

      if (button.result_file === null) {
        alert(`En la prueba ${button.id} no se introdujo ningún fichero de resultado`);
        is_possible_to_send_files = false;
      }

      if (button.puntuation <= 0) {
        alert(`En la prueba ${button.id} no se introdujo una puntuación mayor a 0`);
        is_possible_to_send_files = false;
      }
    })}

    if (is_possible_to_send_files === false) { return; }

    let get_block_id = block_name[block_name.length - 1]
    let get_question_id = question_name[question_name.length - 1]
    if (activate_function_update === false) {
      activate_function_update = true
      try { // Guardamos la info de la pregunta en el JSON de registro
        const response = await fetch(route_to_server + 'regist-question-admin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: get_block_id,
            question_id: get_question_id, 
            tittle: title,
            description: description
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
    } else {
      try { // Guardamos la info de la pregunta en el JSON de registro
        const response = await fetch(route_to_server + 'update-current-question', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            text: get_block_id,
            question_id: get_question_id, 
            tittle: title,
            description: description
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

    // Enviar archivos
    const formData = new FormData();
    formData.append('text', block_name);
    formData.append('question_name', question_name);

    buttons.forEach((button) => {
      const fileInput = document.getElementById(`fileInput_${button.id}`).files[0];
      if (fileInput) {
        formData.append('files', fileInput);
      }
      const resultFileInput = document.getElementById(`fileResult_${button.id}`).files[0];
      if (resultFileInput) {
        formData.append('resultFiles', resultFileInput);
      }
    });
      
    try { // Guardamos la info de la pregunta en el JSON de registro
      const response = await fetch(route_to_server + 'upload-admin-test-to-question-folder', {
        method: 'POST',
        body: formData,
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

    let previous_route = "block_internal_admin_page/" + block_name
    alert("Información registrada con éxito")
    navigate(`/${previous_route}`)  
  };

  const SendFileUser = async () => {
    if (uploadedFiles.fileUser === null) {
      alert("Error. No se ha subido ninguna entrada")
      return;
    }

    const fileInput = document.getElementById('fileInputUser').files[0];
    const formData = new FormData();
    formData.append('file', fileInput); 
    formData.append('userName', userName); 
    formData.append('blockName', block_name);
    formData.append('questionName', question_name);

    try {
      const response = await fetch(route_to_server + 'upload-file-user', {
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
          <input key={id} type="text" value={title} onChange={handleTitleChange} className="title_input_admin" placeholder="Escriba el título aquí"/>
        </div>
        <div className="description_question_page_admin">
          <input key={id} type="text" value={description} onChange={handleDescriptionChange} className="description_input_admin" placeholder="Escriba la descripción aquí"/>
        </div>
        {buttons.map((button) => (
        <div key={button.id} className="puntuation_question_page_admin">
          <button className="button_submit_test" onClick={() => document.getElementById(`fileInput_${button.id}`).click()}>{content_of_button_admin_enter_file}</button>
          <input id={`fileInput_${button.id}`} type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, button.id)} />
          {button.file && <span className="file_name_display">{button.file}</span>}

          <button className="button_submit_test_2" onClick={() => document.getElementById(`fileResult_${button.id}`).click()}>{content_of_button_admin_result_file}</button>
          <input id={`fileResult_${button.id}`} type="file" style={make_invisible} onChange={(e) => handleResultFileUpload(e, button.id)} />
          {button.result_file && <span className="file_name_display">{button.result_file}</span>}

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
        {buttons.length >= 1 && (
          <button className="button_change_to_admin_or_monitor_activated" onClick={ChangePermission}>Probar cómo usuario</button>
        )}
      </div>
    );
  } else if (isTemporalyUser === true) {
    return(
      <div className="App_question_page_user">
        <div className="tittle_question_page_admin">
          <input key={id} type="text" value={title} className="title_input_admin" readOnly/>
        </div>
        <div className="description_question_page_admin">
          <input key={id} type="text" value={description} className="description_input_admin" readOnly/>
        </div>
        <div className="user_submit_code">
          <button className="button_submit_code" onClick={() => triggerFileInputUser('fileInputUser')}>{content_of_button_user}</button>
          <input id="fileInputUser" type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, 'fileUser')} />
          {uploadedFiles.fileUser && <span className="file_name_display_user">{uploadedFiles.fileUser}</span>}
        </div>
        <div className="user_submit_code">
          <button className="button_submit_code" onClick={SendFileUser}>Confirmar</button>
        </div>
        <button className="button_change_to_admin_or_monitor_activated" onClick={ChangePermission}>
          Volver al rol anterior
        </button>
      </div>
    )
  } else {
    return (
      <div className="App_question_page_user">
        <div className="tittle_question_page_admin">
          <input key={id} type="text" value={title} className="title_input_admin" readOnly/>
        </div>
        <div className="description_question_page_admin">
          <input key={id} type="text" value={description} className="description_input_admin" readOnly/>
        </div>
        <div className="user_submit_code">
          <button className="button_submit_code" onClick={() => triggerFileInputUser('fileInputUser')}>{content_of_button_user}</button>
          <input id="fileInputUser" type="file" style={make_invisible} onChange={(e) => handleFileUpload(e, 'fileUser')} />
          {uploadedFiles.fileUser && <span className="file_name_display_user">{uploadedFiles.fileUser}</span>}
        </div>
        <div className="user_submit_code">
          <button className="button_submit_code" onClick={SendFileUser}>Confirmar</button>
        </div>
      </div>
    )
  }
};
