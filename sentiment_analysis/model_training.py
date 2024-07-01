import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments

class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs['labels'] = torch.tensor(label, dtype=torch.long)
        return inputs

def train_model():
    data = pd.read_csv('data/processed_data.csv')
    texts = data['cleaned_content'].tolist()
    labels = data['label'].tolist()
    
    tokenizer = BertTokenizer.from_pretrained('meta/bert-sentiment')
    model = BertForSequenceClassification.from_pretrained('meta/bert-sentiment')
    dataset = SentimentDataset(texts, labels, tokenizer)
    data_loader = DataLoader(dataset, batch_size=8, shuffle=True)
    
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )
    
    trainer.train()

if __name__ == '__main__':
    train_model()
    print("Model training complete")
