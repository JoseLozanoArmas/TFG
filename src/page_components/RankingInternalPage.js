import React, { useState, useEffect } from 'react';
import { Navigate, Route, useNavigate, useParams } from 'react-router-dom';
import './RankingInternalPage.css';

const route_to_server = "http://127.0.0.1:5000/"

export const RankingInternalPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  const [saveJson, setSaveJson] = useState();
  const block_id = "block_1"
  const block_number = 1
  
  const [userSlots, setUserSlots] = useState(() => {
    const savedUserSlots = localStorage.getItem(`user_slots_${id}`);
    if (savedUserSlots) {
      return JSON.parse(savedUserSlots);
    } else {
      return [];
    }
  });

  const getJsonData = async() => {
    try { 
      const response = await fetch(route_to_server + 'get-rankings-info', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: block_id 
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setSaveJson(JSON.parse(data.data))
      } else {
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      alert('Error al conectar con el servidor.');
      console.error(error);
    }
  }

  const getUserInformation = () => {
    for (let i = 0; i < saveJson.length; ++i) {
      alert(saveJson[i].username)
    }
  }

  useEffect(() => {
    getJsonData();
  }, []);

  useEffect(() => {
    localStorage.setItem(`user_slots_${id}`, JSON.stringify(userSlots))
  })
  

  getUserInformation()

  return (
    <div className="App_ranking_internal_page">
      <div className="tittle_ranking_internal_page">
        <h1>Ranking de puntuaciones del bloque {block_number}</h1>
      </div>
      <div>
        
      </div>
    </div>
  )
}