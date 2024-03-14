import torch
from transformers import BertTokenizer

from bert.model import BertClassifier
from bert.train import train
import pandas as pd

EPOCHS = 5
LR = 1e-6
BATCH_SIZE = 4
BASE_PATH = './bert-base-chinese'


train_data = []
val_data = []


print('Loading Bert Tokenizer...')
tokenizer = BertTokenizer.from_pretrained(BASE_PATH)


df = pd.read_excel('./datasets/all_data.xlsx')
labels = ['无', '接受', '记忆', '应用', '提问', '阐述', '创造', '支持', '反对', '讨论']
for index, row in df.iterrows():
  text = str(row['Value'])
  label = str(row['table'])

  li = labels.index(label) if label in labels else 0
  label = torch.zeros(len(labels))
  label[li] = 1

  bert_input = tokenizer(text, padding='max_length', max_length=10, truncation=True, return_tensors="pt")

  if index % 10 == 0:
    val_data.append([bert_input, label])
  else:
    train_data.append([bert_input, label])
print(f"Train Data: {len(train_data)}")
print(f"Val Data: {len(val_data)}\n")


def augmentation_func(data):
  return data


model = BertClassifier()
train(model, train_data, val_data, LR, EPOCHS, BATCH_SIZE, augmentation_func)
