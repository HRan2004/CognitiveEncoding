import torch
import numpy as np
from transformers import BertTokenizer


class Dataset(torch.utils.data.Dataset):
    def __init__(self, data, augmentation_func=None):
      self.data = data
      self.augmentation_func = augmentation_func

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
      if self.augmentation_func is not None:
        item = self.augmentation_func(self.data[idx])
      else:
        item = self.data[idx]
      return item[0], item[1]