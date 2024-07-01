import torch
from transformers import BertTokenizer, BertForSequenceClassification

def load_model():
    tokenizer = BertTokenizer.from_pretrained('./model')
    model = BertForSequenceClassification.from_pretrained('./model')
    return tokenizer, model

if __name__ == '__main__':
    tokenizer, model = load_model()
    print("Model loaded successfully")
