// components/MainPage.jsx
import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import './styles/main.css';
import { UserContext } from '../UserContext';
import AdCard from './AdCard';

const MainPage = () => {
  const { user } = useContext(UserContext);
  const [ads, setAds] = useState([]);

  useEffect(() => {
    const fetchAds = async () => {
      try {
        const response = await axios.get('http://localhost:8000/get_ad');
        setAds(response.data);
      } catch (error) {
        console.error('Error fetching ads:', error);
      }
    };

    fetchAds();
  }, []);

  return (
    <div className="main-content">
      <div className="ads-container">
        {ads.map(ad => (
          <AdCard key={ad.ad_id} ad_id={ad.ad_id} photo={ad.photo} title={ad.title} />
        ))}
      </div>
    </div>
  );
};

export default MainPage;
