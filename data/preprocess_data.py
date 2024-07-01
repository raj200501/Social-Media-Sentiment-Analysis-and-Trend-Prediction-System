import pandas as pd
import re

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\W', ' ', text)
    text = text.lower().strip()
    return text

def preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data['cleaned_content'] = data['content'].apply(preprocess_text)
    data.to_csv('data/processed_data.csv', index=False)

if __name__ == '__main__':
    preprocess_data('data/sample_data.csv')
    print("Data preprocessing complete")
