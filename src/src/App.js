import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';
import { QuestionPageUser } from './page_components/QuestionPageUser';

const Home = () => {
  const navigate = useNavigate();

  const GoToQuestionPageUser = () => {
    navigate('/question_user'); 
  };

  const [user_name, setTexto] = useState('');
  const [variableGuardada, setVariableGuardada] = useState('');

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

        setVariableGuardada(user_name);
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
          <textarea value={user_name} onChange={(e) => setTexto(e.target.value)} placeholder="Inserte nombre de usuario..."></textarea>
          <button onClick={SaveUser}>Guardar Texto</button>
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
      </Routes>
    </Router>
  );
}

export default App;
