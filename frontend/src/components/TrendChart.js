import React from 'react';
import { Line } from 'react-chartjs-2';

const TrendChart = ({ data, trendName }) => {
  const chartData = {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: trendName,
        data: data.map(item => item.count),
        fill: false,
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgba(255, 99, 132, 0.2)',
      },
    ],
  };

  return <Line data={chartData} />;
};

export default TrendChart;
