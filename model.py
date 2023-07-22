import tensorflow as tf

'''
RuleModel:
- Take input of neighbours of cell as input.
- Take input of desired state after rule applied.
- Train model based on all inputs.
- Given set of neighbours of cell, output dead or alive. 
'''
class RuleModel:
    def __init__(self) -> None:
        self.inputs = []
        self.model = None


    def encode_state(self, alive, neighbours):
        input = []
        input.append(1 if alive else 0)
        for neighbour in neighbours:
            input.append(1 if neighbour else 0)
        return input
    

    def add_state(self, alive: bool, neighbours: list, output: bool) -> None:
        input = self.encode_state(alive, neighbours)
        if input not in self.inputs:
            self.inputs.append([input, output])


    def train_model(self) -> None:
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input((9,)),
            tf.keras.layers.Dense(9, activation='relu'),
            tf.keras.layers.Dense(1)
        ])

        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
            metrics=['BinaryAccuracy']
        )

        keys = [i[0] for i in self.inputs]
        values = [i[1] for i in self.inputs]

        self.model.fit(keys, values, epochs=5)

        
    async def make_prediction(self, alive: bool, neighbours: list) -> bool:
        input = self.encode_state(alive, neighbours)
        return self.model.predict([input])