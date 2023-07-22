from screens import RuleScreen, GameScreen


if __name__ == "__main__":
    # Rule Creation Screen
    screen1 = RuleScreen()

    # Standard GOL Rules
    USE_STANDARD_RULES = [
        lambda alive, neighbours : alive and (sum(neighbours) == 2 or sum(neighbours) == 3),
        lambda alive, neighbours : not alive and sum(neighbours) == 3
    ] 
    # Model's Predicted Rules
    USE_MODEL_RULES = [
        lambda alive, neighbours : screen1.make_prediction(alive, neighbours)
    ]

    # If any inputs were created
    if screen1.model:
        screen2 = GameScreen(USE_MODEL_RULES)
    else:
        screen2 = GameScreen(USE_STANDARD_RULES)