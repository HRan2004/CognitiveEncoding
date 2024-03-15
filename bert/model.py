from torch import nn
from transformers import BertModel


class BertClassifier(nn.Module):
    def __init__(self, base_path, dropout=0.5):
        super(BertClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(base_path)
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(1024, 10)
        # self.linear2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):
        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        # linear2_output = self.linear2(linear_output)
        final_layer = self.relu(linear_output)
        return final_layer