import tensorflow as tf
import random
import datetime

class RulesetModel:
    def __init__(self, rule_count, alive_rule_limit):
        self.rule_count = rule_count
        self.alive_rule_limit = alive_rule_limit
        self.model = None
        self.inputs = self.create_dataset()

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

    def create_model(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input((9,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32),
            tf.keras.layers.Dense(1)
        ])

        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
            metrics=['BinaryAccuracy']
        )

    def train_model(self):
        keys = tf.convert_to_tensor([i[0] for i in self.inputs])
        values = tf.convert_to_tensor([i[1] for i in self.inputs])

        print(f"[{datetime.datetime.now()}]: Training model...")
        self.model.fit(keys, values, epochs=10)

    def get_model(self):
        return self.model