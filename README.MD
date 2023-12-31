# Brophy's Game Of Life
This project was an introduction to my own private study of Machine Learning (ML) outside of education. Conway's Game of Life is an interesting piece of cellular automota and I wanted to put my own spin on it. I wanted to develop my own informal understanding of ML during the summer before continuing my formal education in the subject in September.


## Running the Game
Requirements:
- Pygame
- Tensorflow

Install each of the above libraries. Run main.py.

RuleScreen:
Click the cells to switch them on or off. Clicking the input cell (left) will switch it from being alive to dead or vice versa. Same goes for the output cell (right).

GameScreen:
Add cells like normal CGOL. If inputs were made on the RuleScreen, the ML model will be used to determine a cells state. Otherwise, standard CGOL rules will apply.


## Approach
These were the stages of development:
- Create basic Conway's Game of Life (CGOL) ran on the command line.
- Output to Pygame interface instead of the command line.
- Refactor CGOL so that it could be used on an infinite grid.
- Create a basic Machine Learning model.
- Create RuleScreen to create inputs for the ML model.
- Connect the model to the GameScreen if inputs were made.
