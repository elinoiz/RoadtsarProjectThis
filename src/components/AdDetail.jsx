import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './styles/adDetail.css';

const AdDetail = () => {
  const { ad_id } = useParams();
  const [ad, setAd] = useState(null);
  const [bids, setBids] = useState([]); // Состояние для хранения ставок
  const [showModal, setShowModal] = useState(false);
  const [bidAmount, setBidAmount] = useState('');

  useEffect(() => {
    const fetchAd = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/get_ad/${ad_id}`);
        setAd(response.data);
      } catch (error) {
        console.error('Error fetching ad:', error);
      }
    };

    const fetchBids = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/get_bids/${ad_id}`);
        setBids(response.data);
      } catch (error) {
        console.error('Error fetching bids:', error);
      }
    };

    fetchAd();
    fetchBids();
  }, [ad_id]);

  const handleBid = async () => {
    try {
      const userId = localStorage.getItem('user'); // Предполагается, что ID пользователя хранится в localStorage
      if (userId) {
        await axios.post('http://localhost:8000/place_bid', {
          ad_id: ad_id,
          user_id: JSON.parse(userId).user_id,
          bid_amount: bidAmount
        });
        setShowModal(false);
        setBidAmount('');
        alert('Ставка успешно размещена!');
      } else {
        alert('Пожалуйста, войдите в систему, чтобы сделать ставку.');
      }
    } catch (error) {
      console.error('Error placing bid:', error);
    }
  };

  if (!ad) {
    return <div>Loading...</div>;
  }

  return (
    <div className="ad-detail">
      <div className="left-section">
        <img src={`data:image/jpeg;base64,${ad.photo}`} alt={ad.title} />
        <button onClick={() => setShowModal(true)}>Сделать ставку</button>
      </div>
      <div className="right-section">
        <h2>{ad.title}</h2>
        <p><strong>Город:</strong> {ad.city}</p>
        <p><strong>Начальная цена:</strong> {ad.start_price}</p>
        <p><strong>Категория:</strong> {ad.category}</p>
        <p><strong>Описание:</strong> {ad.description}</p>
        <div className="bids-section">
          <h3>Ставки:</h3>
          {bids.length > 0 ? (
            <table className="bids-table">
              <thead>
                <tr>
                  <th>Имя пользователя</th>
                  <th>Ставка</th>
                </tr>
              </thead>
              <tbody>
                {bids.map((bid) => (
                  <tr key={bid.bid_id}>
                    <td>{bid.user_name}</td>
                    <td>{bid.bid_amount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Нет ставок</p>
          )}
        </div>
      </div>

      <div className={`modal ${showModal ? 'show' : ''}`} onClick={() => setShowModal(false)}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <h2>Сделать ставку</h2>
          <input
            type="number"
            value={bidAmount}
            onChange={(e) => setBidAmount(e.target.value)}
            placeholder="Введите сумму ставки"
          />
          <button onClick={handleBid}>ОК</button>
        </div>
      </div>
    </div>
  );
};

export default AdDetail;
