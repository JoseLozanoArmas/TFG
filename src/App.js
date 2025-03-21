import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';
import { UserPageAdmin } from './page_components/UserPageAdmin';
import { BlockGeneralAdminPage } from './page_components/BlockGeneralAdminPage';
import { BlockInternalAdminPage } from './page_components/BlockInternalAdminPage';
import { QuestionPageAdmin } from './page_components/QuestionPageAdmin';
import { ControlPanel } from './page_components/ControlPanel';
import { RankingPageAdmin } from './page_components/RankingPageAdmin';
import { DeleteOptions } from './page_components/DeleteOptions';
import { Settings } from './page_components/Settings';
import { GeneralUserPage } from './page_components/GeneralUserPage';
import { InternalUserPage } from './page_components/InternalUserPage';
import { RankingInternalPage } from './page_components/RankingInternalPage';

export const route_to_server = "http://127.0.0.1:5000/"

const Home = () => {
  const navigate = useNavigate();

  const GoToQuestionPageUser = () => {
    navigate('/block_general_admin_page'); 
  };

  const GoToAdminPageUser = () => {
    navigate('/admin_page_user'); 
  }

  const [user_name, saveUserName] = useState('');

  const SaveUser = async () => {
    if (!user_name.trim()) { 
      alert('Por favor introduzca un nombre de usuario.');
      return;
    }

    try { // Crear la carpeta del usuario
      const response = await fetch(route_to_server + 'save-user-name', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: user_name }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        //alert(data.message);
        localStorage.setItem("user_role", "user"); 
        localStorage.setItem("name_user", user_name);
        GoToQuestionPageUser();
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={require('./img/user_img.png')} alt="User" className="user-image" />
        <div className="input-box">
          {"Login"}
          <textarea value={user_name} onChange={(e) => saveUserName(e.target.value)} placeholder="Inserte nombre de usuario..."></textarea>
          <button onClick={SaveUser}>Iniciar</button>
          <button className="admin_button" onClick={GoToAdminPageUser}>¿Entrar cómo docente?</button>
        </div>
      </header>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin_page_user" element={<UserPageAdmin />} />
        <Route path="/block_general_admin_page" element={<BlockGeneralAdminPage />} />
        <Route path="/block_internal_admin_page/:id" element={<BlockInternalAdminPage/>} />
        <Route path="/:id" element={<QuestionPageAdmin/>}/>
        <Route path="/control_panel" element={<ControlPanel/>}/>
        <Route path="/ranking" element={<RankingPageAdmin/>}/>
        <Route path="/settings" element={<Settings/>}/>
        <Route path="/delete_options" element={<DeleteOptions/>}/>
        <Route path="/general_users" element={<GeneralUserPage/>}/>
        <Route path="/creation_user/:id" element={<InternalUserPage/>}/>
        <Route path="/ranking_internal_page/:id" element={<RankingInternalPage/>}/>
      </Routes>
    </Router>
  );
}

export default App;
