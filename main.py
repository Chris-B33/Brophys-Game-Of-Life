import configparser as cp
import datetime

from src.model import RulesetTrainer
from src.screen import GameScreen

if __name__ == "__main__":
    config = cp.ConfigParser()
    config.read(r"config.ini")
    rule_count = int(config.get("model-parameters", "rule_count"))
    alive_rule_limit = int(rule_count * float(config.get("model-parameters", "dead_to_alive_rule_proportion")))

    print(f"[{datetime.datetime.now().time()}]: Initializing model...")
    game_model = RulesetTrainer(rule_count, alive_rule_limit)

    print(f"[{datetime.datetime.now().time()}]: Training model...")
    game_model.train_model()

    print(f"[{datetime.datetime.now().time()}]: Running Game...")
    screen = GameScreen(game_model.get_model())