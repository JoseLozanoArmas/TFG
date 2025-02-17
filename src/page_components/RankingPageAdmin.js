import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './RankingPageAdmin.css';

const route_to_server = "http://127.0.0.1:5000/"

export const RankingPageAdmin = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [saveJson, setSaveJson] = useState();

  const [blockButtons, setblockButtons] = useState(() => {
    const savedblockButtons = localStorage.getItem(`block_buttons_${id}`);
    if (savedblockButtons) {
      return JSON.parse(savedblockButtons);
    } else {
      return [];
    }
  });

  useEffect(() => {
    const getJsonData = async () => {
      try {
        const response = await fetch(route_to_server + 'get-data-blocks-buttons-json');
        const data = await response.json();
        if (response.ok) {
          setSaveJson(JSON.parse(data.data));  // Guardamos el contenido en el estado
        } else {
          console.error(`Error: ${data.error}`);
        }
      } catch (error) {
        console.error('Error al obtener los datos del servidor', error);
      }
    };
    getJsonData();
  }, []);


  useEffect(() => {
    if (!saveJson) { return; }
    const getUserInformation = () => {
      let save_buttons = []
      for (let i = 0; i < saveJson.length; ++i) {
        save_buttons.push(saveJson[i]);
      }
      setblockButtons(save_buttons)
    }
    getUserInformation();
  }, [saveJson])


  useEffect(() => {
    localStorage.setItem(`block_buttons_${id}`, JSON.stringify(blockButtons))
  })

  const MoveToRankingPage = (id) => {
    navigate(`/ranking_internal_page/${id}`)
  }

  // localStorage.clear()

  return (
    <div className="App_ranking_general_page">
      <div className="tittle_general_ranking_page">
        <h1>Mapa general de los Rankings</h1>  
      </div>
      {blockButtons.map((button) => (
        <button key={button.id} className="image-button" style={{transform: `translate(${button.positionX}px, ${button.positionY}px)`}}
          onClick={() => MoveToRankingPage(button.block_name)}>
          <img src={require("../img/logo_ull.png")} className="user-image"/>
        </button>
      ))}
    </div>
  );
};
