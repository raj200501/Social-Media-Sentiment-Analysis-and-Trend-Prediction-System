import pandas as pd
import matplotlib.pyplot as plt

def plot_trend(trends, trend_idx):
    trend_words = trends[trend_idx]
    data = pd.read_csv('data/processed_data.csv')
    data['created_at'] = pd.to_datetime(data['created_at'])
    
    trend_data = data[data['cleaned_content'].apply(lambda x: any(word in x for word in trend_words))]
    trend_data = trend_data.set_index('created_at').resample('D').count()
    
    plt.figure(figsize=(10, 6))
    plt.plot(trend_data['content'])
    plt.title(f"Trend {trend_idx+1}: {', '.join(trend_words)}")
    plt.xlabel("Date")
    plt.ylabel("Frequency")
    plt.show()

def main():
    trends = [
        ['meta', 'ai', 'machine', 'learning', 'model'],
        ['social', 'media', 'facebook', 'instagram', 'post'],
        # More trends...
    ]
    plot_trend(trends, 0)

if __name__ == '__main__':
    main()
    print("Trend analysis complete")
