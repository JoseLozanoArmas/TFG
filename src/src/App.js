import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';
import { QuestionPageUser } from './page_components/QuestionPageUser';
import { UserPageAdmin } from './page_components/UserPageAdmin';
import { BlockGeneralAdminPage } from './page_components/BlockGeneralAdminPage';

const Home = () => {
  const navigate = useNavigate();

  const GoToQuestionPageUser = () => {
    navigate('/question_user'); 
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

    try {
      const response = await fetch('http://127.0.0.1:5000/save-user-name', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: user_name }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        alert(data.message); 
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
          <button className="admin_button" onClick={GoToAdminPageUser}>¿Entrar cómo administrador?</button>
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
        <Route path="/question_user" element={<QuestionPageUser />} />
        <Route path="/admin_page_user" element={<UserPageAdmin />} />
        <Route path="/block_general_admin_page" element={<BlockGeneralAdminPage />} />
      </Routes>
    </Router>
  );
}

export default App;
