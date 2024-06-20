// components/AdCard.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/adCard.css';

const AdCard = ({ ad_id, photo, title }) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/main/ad/${ad_id}`);
  };

  return (
    <div className="ad-card" onClick={handleCardClick}>
      <img src={`data:image/jpeg;base64,${photo}`} alt={title} className="ad-photo" />
      <div className="ad-title">{title}</div>
    </div>
  );
};

export default AdCard;
