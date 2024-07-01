import pandas as pd
from fbprophet import Prophet

def predict_trend(trend_idx):
    trends = [
        ['meta', 'ai', 'machine', 'learning', 'model'],
        ['social', 'media', 'facebook', 'instagram', 'post'],
        # More trends...
    ]
    trend_words = trends[trend_idx]
    data = pd.read_csv('data/processed_data.csv')
    data['created_at'] = pd.to_datetime(data['created_at'])
    
    trend_data = data[data['cleaned_content'].apply(lambda x: any(word in x for word in trend_words))]
    trend_data = trend_data.set_index('created_at').resample('D').count()
    
    df = trend_data.reset_index()[['created_at', 'content']]
    df.columns = ['ds', 'y']
    
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    model.plot(forecast)
    model.plot_components(forecast)
    plt.show()

def main():
    predict_trend(0)

if __name__ == '__main__':
    main()
    print("Trend prediction complete")
