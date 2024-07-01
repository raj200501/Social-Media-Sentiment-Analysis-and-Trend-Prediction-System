import torch
from transformers import BertTokenizer, BertForSequenceClassification

model_name = "meta/bert-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    sentiment = torch.argmax(outputs.logits, dim=-1).item()
    return sentiment
