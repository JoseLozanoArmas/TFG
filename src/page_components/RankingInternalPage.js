import React, { useState, useEffect } from 'react';
import { Navigate, Route, useNavigate, useParams } from 'react-router-dom';
import './RankingInternalPage.css';

const route_to_server = "http://127.0.0.1:5000/"

export const RankingInternalPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  const [saveJson, setSaveJson] = useState(null);
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

  useEffect(() => {
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
          setSaveJson(JSON.parse(data.data));
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (error) {
        alert('Error al conectar con el servidor.');
        console.error(error);
      }
    }
    getJsonData();
  }, []);

  useEffect(() => {
    if (!saveJson) { return; }
    const getUserInformation = () => {
      let save_slots = []
      for (let i = 0; i < saveJson.length; ++i) {
        saveJson[i]["id"] = i + 1;
        save_slots.push(saveJson[i])
      }
      setUserSlots(save_slots)
    }
    getUserInformation();
  }, [saveJson])

  useEffect(() => {
    localStorage.setItem(`user_slots_${id}`, JSON.stringify(userSlots))
  })

  

  return (
    <div className="App_ranking_internal_page">
      <div className="tittle_ranking_internal_page">
        <h1>Ranking de puntuaciones del bloque {block_number}</h1>
      </div>
      <div className="user_slot">
          <div className="slot_id">
            Posición
          </div>
          <div className="slot_username">
            Usuario
          </div>
          <div className="slot_puntuation">
            Puntuación
          </div>
          <div className="slot_time">
            Tiempo total
          </div>
      </div>
      {userSlots.map((slot) => (
        <div key={slot.id} className="user_slot">
          <div className="slot_id">
            {slot.id}
          </div>
          <div className="slot_username">
            {slot.username}
          </div>
          <div className="slot_puntuation">
            {slot.puntuation}
          </div>
          <div className="slot_time">
            {slot.time}
          </div>
        </div>
      ))}
    </div>
  )
}