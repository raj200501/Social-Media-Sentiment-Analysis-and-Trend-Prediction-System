import torch
from transformers import BertTokenizer, BertForSequenceClassification

def save_model():
    tokenizer = BertTokenizer.from_pretrained('meta/bert-sentiment')
    model = BertForSequenceClassification.from_pretrained('meta/bert-sentiment')
    model.save_pretrained('./model')
    tokenizer.save_pretrained('./model')

if __name__ == '__main__':
    save_model()
    print("Model saved successfully")
