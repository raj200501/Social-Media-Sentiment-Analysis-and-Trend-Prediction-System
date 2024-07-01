import React from 'react';
import { Line } from 'react-chartjs-2';

const SentimentChart = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: 'Sentiment Score',
        data: data.map(item => item.score),
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return <Line data={chartData} />;
};

export default SentimentChart;
