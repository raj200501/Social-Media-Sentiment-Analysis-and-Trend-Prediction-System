const apiBase = "http://localhost:5000";

function drawLineChart(canvas, labels, values, color) {
  const ctx = canvas.getContext("2d");
  const padding = 40;
  const width = canvas.width - padding * 2;
  const height = canvas.height - padding * 2;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "#dfe6f1";
  ctx.lineWidth = 1;

  for (let i = 0; i <= 5; i += 1) {
    const y = padding + (height / 5) * i;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(padding + width, y);
    ctx.stroke();
  }

  if (values.length === 0) {
    return;
  }

  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);
  const range = maxValue - minValue || 1;

  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  values.forEach((value, index) => {
    const x = padding + (width / (values.length - 1 || 1)) * index;
    const y = padding + height - ((value - minValue) / range) * height;
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.stroke();

  ctx.fillStyle = "#1a1a1a";
  ctx.font = "12px sans-serif";
  ctx.fillText(labels[0], padding, canvas.height - 10);
  ctx.fillText(labels[labels.length - 1], canvas.width - padding - 50, canvas.height - 10);
}

async function fetchSentimentData() {
  const response = await fetch(`${apiBase}/api/sentiment_data`);
  return response.json();
}

async function fetchTrendData() {
  const response = await fetch(`${apiBase}/api/trend_data`);
  return response.json();
}

async function fetchForecast(trend) {
  const response = await fetch(`${apiBase}/api/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ trend, days: 7 }),
  });
  return response.json();
}

async function analyzeSentiment(text) {
  const response = await fetch(`${apiBase}/api/sentiment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  return response.json();
}

async function init() {
  const sentimentData = await fetchSentimentData();
  const sentimentLabels = sentimentData.map((item) => item.date);
  const sentimentScores = sentimentData.map((item) => item.score);
  drawLineChart(
    document.getElementById("sentiment-chart"),
    sentimentLabels,
    sentimentScores,
    "#1f4b99"
  );

  const trendData = await fetchTrendData();
  document.getElementById("trend-title").textContent = `Trending Topic: ${trendData.trend}`;
  const trendLabels = trendData.series.map((item) => item.date);
  const trendCounts = trendData.series.map((item) => item.count);
  drawLineChart(
    document.getElementById("trend-chart"),
    trendLabels,
    trendCounts,
    "#4b9f7f"
  );

  const sentimentButton = document.getElementById("sentiment-submit");
  sentimentButton.addEventListener("click", async () => {
    const input = document.getElementById("sentiment-input");
    const resultContainer = document.getElementById("sentiment-result");
    const result = await analyzeSentiment(input.value);
    if (result.error) {
      resultContainer.textContent = result.error;
      return;
    }
    const { label, score } = result.result;
    resultContainer.textContent = `Label: ${label} (score ${score})`;
  });

  const forecastButton = document.getElementById("forecast-button");
  forecastButton.addEventListener("click", async () => {
    const forecast = await fetchForecast(trendData.trend);
    const list = document.getElementById("forecast-list");
    list.innerHTML = "";
    forecast.forecast.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `Day ${item.day}: ${item.count}`;
      list.appendChild(li);
    });
  });
}

init().catch((error) => {
  console.error("Failed to initialize dashboard", error);
});
