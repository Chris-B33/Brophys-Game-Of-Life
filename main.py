import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
import configparser as cp
import random
import datetime

from src.screen import GameScreen

if __name__ == "__main__":
    config = cp.ConfigParser()
    config.read(r"config.ini")
    rule_count = int(config.get("model-parameters", "rule_count"))
    alive_rule_limit = int(rule_count * float(config.get("model-parameters", "dead_to_alive_proportion")))

    # Create Dataset
    print(f"[{datetime.datetime.now()}]: Creating dataset...")
    inputs = []
    alive_rule_count = 0
    for i in range(rule_count):
        rule = [random.choice([True, False]) for _ in range(9)]
        output = True
        
        if output and alive_rule_count < alive_rule_limit:
            alive_rule_count += 1
        else:
            output = False

        inputs.append([rule, output])

    # Train Model
    print(f"[{datetime.datetime.now()}]: Creating model...")
    model = tf.keras.Sequential([
        tf.keras.layers.Input((9,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32),
        tf.keras.layers.Dense(1)
    ])

    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
        metrics=['BinaryAccuracy']
    )

    keys = tf.convert_to_tensor([i[0] for i in inputs])
    values = tf.convert_to_tensor([i[1] for i in inputs])

    print(f"[{datetime.datetime.now()}]: Training model...")
    model.fit(keys, values, epochs=10)

    # Run game
    screen = GameScreen(model)