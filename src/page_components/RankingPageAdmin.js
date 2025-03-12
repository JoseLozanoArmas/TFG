import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './RankingPageAdmin.css';
import { route_to_server } from '../App';

export const RankingPageAdmin = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [saveJson, setSaveJson] = useState();

  useEffect(() => {
    const getJsonData = async () => { // Guardamos las posiciones de los botones
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


  const [blockButtons, setblockButtons] = useState([]);


  useEffect(() => {
    if (!saveJson) { return; }
    const getUserInformation = () => { // Guardamos los datos de registro de los usuarios
      let save_buttons = []
      for (let i = 0; i < saveJson.length; ++i) {
        save_buttons.push(saveJson[i]);
      }
      setblockButtons(save_buttons)
    }
    getUserInformation();
  }, [saveJson]);

  const MoveToRankingPage = (id) => {
    navigate(`/ranking_internal_page/${id}`)
  }

  return (
    <div className="App_ranking_general_page">
      <div className="tittle_general_ranking_page">
        <h1>Mapa general de los Rankings</h1>  
      </div>
      {blockButtons.map((button) => (
        <button key={button.id} className="image-button" style={{transform: `translate(${button.positionX}px, ${button.positionY}px)`}}
          onClick={() => MoveToRankingPage(button.block_name)}>
          <img src={require("../img/logo_ull.png")} className="user-image"/>
          <span className="label-name"> Bloque {button.id} </span>
        </button>
      ))}
    </div>
  );
};
