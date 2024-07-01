import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def detect_trends(texts, n_topics=5):
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = vectorizer.fit_transform(texts)
    nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
    
    feature_names = vectorizer.get_feature_names_out()
    trends = []
    for topic_idx, topic in enumerate(nmf.components_):
        trends.append([feature_names[i] for i in topic.argsort()[:-11:-1]])
    
    return trends

def main():
    data = pd.read_csv('data/processed_data.csv')
    texts = data['cleaned_content'].tolist()
    trends = detect_trends(texts)
    for idx, trend in enumerate(trends):
        print(f"Trend {idx+1}: {', '.join(trend)}")

if __name__ == '__main__':
    main()
    print("Trend detection complete")
