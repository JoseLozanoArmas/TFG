import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './GeneralUserPage.css';

export const GeneralUserPage = () => {
  const navigate = useNavigate();
  const maxPageWidth = window.innerWidth - 100;
  const userHeight = 155;
  const [isAdmin, setIsAdmin] = useState(false);

  // localStorage.clear();
  
  useEffect(() => {
  const userRole = localStorage.getItem('user_role');
    setIsAdmin(userRole === 'admin');
  }, []);

  const [users, setUsers] = useState(() => {
    const saveUsers = localStorage.getItem('users');
    if (saveUsers) {
      return JSON.parse(saveUsers);
    } else {
      return [{ id: 1, positionX: 0, positionY: 0, type: 'button_plus' }];
    }
  });

  const [userHistory, setUserHistory] = useState(() => {
    const savedHistory = localStorage.getItem('userHistory');
    if (savedHistory) {
      return JSON.parse(savedHistory);
    } else {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('users', JSON.stringify(users));
    localStorage.setItem('userHistory', JSON.stringify(userHistory));
  }, [users, userHistory]);

  const handleButtonPlusClick = async (id) => {
    const clickedUser = users.find((user) => user.id === id);
    if (!clickedUser) {
      console.error('Botón no encontrado.');
      return;
    }
    const newPositionX = clickedUser.positionX + 200;
    let positionX = 0;
    if (newPositionX >= maxPageWidth) {
      positionX = 0;
    } else {
      positionX = newPositionX;
    }

    let positionY = 0;
    if (newPositionX >= maxPageWidth) {
      positionY = clickedUser.positionY + userHeight;
    } else {
      positionY = clickedUser.positionY;
    }

    const updatedUser = { ...clickedUser, positionX, positionY,};
    setUserHistory((prevHistory) => [...prevHistory, { positionX: clickedUser.positionX, positionY: clickedUser.positionY },]);
  
    const newUser = {
      id: users.length + 1,
      positionX: clickedUser.positionX,
      positionY: clickedUser.positionY,
      type: 'user',
    };
  
    setUsers((prevUsers) => [
      ...prevUsers.map((user) => (user.id === id ? updatedUser : user)),
      newUser,
    ]);    
  };

  const removeLastUser = async () => {    
    setUserHistory((prevHistory) => {
        if (prevHistory.length === 0) { return prevHistory; }
        const lastPosition = prevHistory[prevHistory.length - 1];
        setUsers((prevButtons) =>
          prevButtons.map((user) =>
            user.type === 'button_plus' ? { ...user, ...lastPosition } : user
          )
        );
        return prevHistory.slice(0, -1);
      });
      setUsers((prevButtons) => prevButtons.slice(0, -1));
    
  };

  const handleButtonUserClick = async (id) => {
    alert("pendiente")
  }

  return (
    <div className="App3">
      <div className="tittle_block_general_page">
        <h1>Bloque de usuarios</h1>
      </div>
      {users.map((user) => (
        (user.type === 'button_plus' && isAdmin) || user.type !== 'button_plus' ? (
          <button key={user.id} onClick={() => {
            if (user.type === 'button_plus') {
              handleButtonPlusClick(user.id);
            } else {
              handleButtonUserClick(user.id);
            }
          }
        } className="image-button" style={{transform: `translate(${user.positionX}px, ${user.positionY}px)`}}>
        <img src={require(user.type === 'button_plus' ? '../img/icon_plus.png' : '../img/user_img.png')} className="user-image"/>
        </button>
        ) : null
      ))} 
      {users.length > 1 && isAdmin && (
        <button className="button_remove_last" onClick={removeLastUser}>
          Deshacer último usuario
        </button>
      )}
    </div>
  );

}