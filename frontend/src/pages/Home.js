import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SentimentChart from '../components/SentimentChart';
import TrendChart from '../components/TrendChart';

const Home = () => {
  const [sentimentData, setSentimentData] = useState([]);
  const [trendData, setTrendData] = useState([]);
  const [trendName, setTrendName] = useState('');

  useEffect(() => {
    // Fetch sentiment data
    axios.get('/api/sentiment_data')
      .then(response => setSentimentData(response.data))
      .catch(error => console.error(error));

    // Fetch trend data
    axios.get('/api/trend_data')
      .then(response => {
        setTrendData(response.data.data);
        setTrendName(response.data.trendName);
      })
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h1>Social Media Sentiment Analysis and Trend Prediction</h1>
      <h2>Sentiment Over Time</h2>
      <SentimentChart data={sentimentData} />
      <h2>{trendName} Trend Over Time</h2>
      <TrendChart data={trendData} trendName={trendName} />
    </div>
  );
};

export default Home;
