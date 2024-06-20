import React, { useEffect, useContext } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import './styles/main.css';

import logoR from './images/logoR.png';
import iconLoop from './images/iconLoop.png';
import Avatar from './images/Avatar.png';
import icon1 from './images/icon1.png';
import icon2 from './images/icon2.png';
import icon3 from './images/icon3.png';
import icon4 from './images/icon4.png';
import icon5 from './images/icon5.png';
import icon6 from './images/icon6.png';
import icon7 from './images/icon7.png';
import { UserContext } from '../UserContext';

const Layout = () => {
  const { user, setUser } = useContext(UserContext);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, [setUser]);

  const handleSearch = (e) => {
    console.log('Search:', e.target.value);
  };

  const handleCreateAdClick = () => {
    navigate('/main/create-ad');
  };

  return (
    <div>
      <div className="header">
        <img src={logoR} alt="Logo" className="logo" />

        <div className="hat">
          <div className="search-box">
            <input type="text" className="search-input" placeholder="Search..." onChange={handleSearch} />
            <img src={iconLoop} alt="Loop" className="search-icon" />
          </div>

          <div className="roadstar">Roadstar</div>

          <div className="user-info">
            <span className="username">{user ? user.name : 'Александр'}</span>
            <img src={Avatar} alt="Avatar" className="avatar" />
          </div>
        </div>
      </div>

      <div className="left-nav-block">
        <ul className="nav-list">
          <li><img src={icon1} alt="icon1" /> Мои объявления</li>
          <li><img src={icon2} alt="icon2" /> Сообщения</li>
          <li><img src={icon3} alt="icon3" /> Поддержка</li>
          <li><img src={icon4} alt="icon4" /> Мои ставки</li>
          <li><img src={icon5} alt="icon5" /> Контакты</li>
          <li onClick={handleCreateAdClick}><img src={icon6} alt="icon6" /> Создать объявление</li>
          <li><img src={icon7} alt="icon7" /> Настройки</li>
        </ul>
      </div>

      <div className="content">
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;
