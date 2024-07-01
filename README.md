# Social Media Sentiment Analysis and Trend Prediction System

This repository contains the code for a system that uses Meta's AI tools to analyze social media posts for sentiment, detect emerging trends, and predict future trends. The project showcases expertise in NLP, machine learning, and data visualization.

## Features

- Sentiment Analysis (using Meta AI tools)
- Trend Detection
- Trend Prediction
- Data Visualization
- Dockerized Deployment

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js
- Docker
- Docker Compose

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/social-media-sentiment-trend.git
    cd social-media-sentiment-trend
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. Load and preprocess data:
    ```bash
    python data/load_data.py
    python data/preprocess_data.py
    ```

4. Train and evaluate models:
    ```bash
    jupyter notebook notebooks/ModelTraining.ipynb
    ```

5. Run the API server:
    ```bash
    python backend/api/api_server.py
    ```

6. Run the frontend:
    ```bash
    cd frontend
    npm install
    npm start
    ```

## License

This project is licensed under the MIT License.
