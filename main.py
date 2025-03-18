import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import configparser as cp
import datetime

from src.model import RulesetModel
from src.screen import GameScreen

if __name__ == "__main__":
    config = cp.ConfigParser()
    config.read(r"config.ini")
    rule_count = int(config.get("model-parameters", "rule_count"))
    alive_rule_limit = int(rule_count * float(config.get("model-parameters", "dead_to_alive_rule_proportion")))

    print(f"[{datetime.datetime.now()}]: Initializing model...")
    game_model = RulesetModel(rule_count, alive_rule_limit)
    game_model.create_model()

    print(f"[{datetime.datetime.now()}]: Training model...")
    game_model.train_model()

    print(f"[{datetime.datetime.now()}]: Running Game...")
    screen = GameScreen(game_model.get_model())