import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './RankingInternalPage.css';

const route_to_server = "http://127.0.0.1:5000/"

export const RankingInternalPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();


  const [saveJson, setSaveJson] = useState(null);
  const [saveQuestions, setSaveQuestions] = useState(null);
  const block_id = id
  const block_number = block_id[block_id.length - 1]
  
  const [userSlots, setUserSlots] = useState(() => {
    const savedUserSlots = localStorage.getItem(`user_slots_${id}`);
    if (savedUserSlots) {
      return JSON.parse(savedUserSlots);
    } else {
      return [];
    }
  });

  useEffect(() => {
    const getAllQuestions = async() => {
      try { 
        const response = await fetch(route_to_server + 'localize-all-questions-server', {
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
          setSaveQuestions(JSON.parse(data.data));
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (error) {
        alert('Error al conectar con el servidor.');
        console.error(error);
      }
    };
    getAllQuestions();
  },[]);

  useEffect(() => {
    const getJsonData = async() => {
      try { 
        const response = await fetch(route_to_server + 'get-info-student-register', {
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
          if (response.status !== 500) {
            alert(`Error: ${data.message}`);
          }
        }
      } catch (error) {
        alert('Error al conectar con el servidor.');
        console.error(error);
      }
    }
    getJsonData();
  }, []);

  useEffect(() => {
    if (!saveJson || !saveQuestions) return;
    const getUserInformation = () => {
      let save_slots = []
      for (let i = 0; i < saveJson.length; ++i) {
        saveJson[i]["id"] = `${i + 1}º`;
        switch(i) {
          case 0:
            saveJson[i]["id_className"] = "slot_id_gold"
            saveJson[i]["username_className"] = "slot_username_gold"
            saveJson[i]["puntuation_className"] = "slot_puntuation_gold"
            saveJson[i]["time_className"] = "slot_time_gold"
          break;
          case 1:
            saveJson[i]["id_className"] = "slot_id_silver"
            saveJson[i]["username_className"] = "slot_username_silver"
            saveJson[i]["puntuation_className"] = "slot_puntuation_silver"
            saveJson[i]["time_className"] = "slot_time_silver"
          break;
          case 2:
            saveJson[i]["id_className"] = "slot_id_copper"
            saveJson[i]["username_className"] = "slot_username_copper"
            saveJson[i]["puntuation_className"] = "slot_puntuation_copper"
            saveJson[i]["time_className"] = "slot_time_copper"
          break;
          default:
            saveJson[i]["id_className"] = "slot_id"
            saveJson[i]["username_className"] = "slot_username"
            saveJson[i]["puntuation_className"] = "slot_puntuation"
            saveJson[i]["time_className"] = "slot_time"
          break;
        }
        for (let j = 0; j < saveQuestions.length; ++j) {
          if (!saveJson[i][`question_${j + 1}`]) {
            saveJson[i][`question_${j + 1}`] = {points: 0};
            console.log("no está") // TENDRIA QUE DECIR QUE EN ESTA PREGUNTA EL USUARIO TIENE 0 PUNTOS Y NO PONER EL TIEMPO
          } else{
            console.log(saveJson[i][`question_${j + 1}`]) // TENDRIA QUE PONER LOS PUNTOS Y EL TIEMPO SI ES QUE TUVIESE
          }
        }
        save_slots.push(saveJson[i]);
      }
      setUserSlots(save_slots)
    }
    getUserInformation();
  }, [saveJson])

  useEffect(() => {
    localStorage.setItem(`user_slots_${id}`, JSON.stringify(userSlots))
  })

  const MoveToFirstPage = () => {
    navigate('/');
  } 

  return (
    <div className="App_ranking_internal_page">
      <div className="tittle_ranking_internal_page">
        <h1>Ranking de puntuaciones del bloque {block_number}</h1>
      </div>
      <div className="user_slot">
          <div className="slot_id_reference">
            Posición
          </div>
          <div className="slot_username_reference">
            Usuario
          </div>
          {saveQuestions && saveQuestions.map((question) => (
            <div className="slot_id_reference">
              {question.question_id}
            </div>
          ))}
      </div>
      {userSlots.map((slot) => (
        <div key={slot.id} className="user_slot">
          <div className={slot.id_className}>
            {slot.id}
          </div>
          <div className={slot.username_className}>
            {slot.username}
          </div>
          <div className={slot.username_className}>
            {slot.question_1.points}
          </div>
          <div className={slot.username_className}>
            {slot.question_2.points}
          </div>
        </div>
      ))}
      <button className="finish_user" onClick={() => MoveToFirstPage()}> Volver a la página de inicio</button>
    </div>
  )

  /*
  //VERSION ANTIGUA
  return (
    <div className="App_ranking_internal_page">
      <div className="tittle_ranking_internal_page">
        <h1>Ranking de puntuaciones del bloque {block_number}</h1>
      </div>
      <div className="user_slot">
          <div className="slot_id_reference">
            Posición
          </div>
          <div className="slot_username_reference">
            Usuario
          </div>
          <div className="slot_puntuation_reference">
            Puntuación
          </div>
          <div className="slot_time_reference">
            Tiempo total
          </div>
      </div>
      {userSlots.map((slot) => (
        <div key={slot.id} className="user_slot">
          <div className={slot.id_className}>
            {slot.id}
          </div>
          <div className={slot.username_className}>
            {slot.username}
          </div>
          <div className={slot.puntuation_className}>
            {slot.puntuation}
          </div>
          <div className={slot.time_className}>
            {slot.time}
          </div>
        </div>
      ))}
      <button className="finish_user" onClick={() => MoveToFirstPage()}> Volver a la página de inicio</button>
    </div>
  )
    */
}