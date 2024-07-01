from flask import Flask, request, jsonify
from sentiment_analysis.sentiment import analyze_sentiment
from trend_detection.trend_detection import detect_trends
from trend_prediction.prediction import predict_trend

app = Flask(__name__)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_route():
    data = request.get_json()
    content = data['content']
    sentiment = analyze_sentiment(content)
    return jsonify({'sentiment': sentiment})

@app.route('/detect_trends', methods=['GET'])
def detect_trends_route():
    trends = detect_trends()
    return jsonify({'trends': trends})

@app.route('/predict_trend', methods=['POST'])
def predict_trend_route():
    data = request.get_json()
    trend_idx = data['trend_idx']
    prediction = predict_trend(trend_idx)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
