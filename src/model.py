import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(9, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        x = self.fc3(x)
        return x

class RulesetTrainer:
    def __init__(self, rule_count, alive_rule_limit):
        self.rule_count = rule_count
        self.alive_rule_limit = alive_rule_limit
        self.model = Model()
        self.criterion = nn.BCEWithLogitsLoss()
        self.optimizer = optim.Adam(self.model.parameters())

    def create_dataset(self):
        inputs = []
        alive_rule_count = 0

        for _ in range(self.rule_count):
            rule = [random.choice([True, False]) for _ in range(9)]
            output = True

            if output and alive_rule_count < self.alive_rule_limit:
                alive_rule_count += 1
            else:
                output = False

            inputs.append([rule, output])

        return inputs

    def train_model(self):
        inputs = self.create_dataset()

        keys = torch.tensor([i[0] for i in inputs], dtype=torch.float32)
        values = torch.tensor([i[1] for i in inputs], dtype=torch.float32).unsqueeze(1)

        dataset = TensorDataset(keys, values)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

        self.model.train()
        for epoch in range(10):
            for batch_keys, batch_values in dataloader:
                self.optimizer.zero_grad()
                outputs = self.model(batch_keys)
                loss = self.criterion(outputs, batch_values)
                loss.backward()
                self.optimizer.step()

    def get_model(self):
        return self.model