import React, { useState, useEffect } from 'react';
import { Navigate, Route, useNavigate, useParams } from 'react-router-dom';
import './RankingInternalPage.css';

const route_to_server = "http://127.0.0.1:5000/"

export const RankingInternalPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  const block_id = "1"

  return (
    <div className="App_ranking_internal_page">
      <div className="tittle_ranking_internal_page">
        <h1>Ranking de puntuaciones del bloque {block_id}</h1>
      </div>
    </div>
  )
}