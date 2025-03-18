import tensorflow as tf

class GameOfLife:
    ADJACENT = (
        (-1,-1), (0,-1), (1,-1),
        (-1, 0),         (1, 0),
        (-1, 1), (0, 1), (1, 1)
    )

    def __init__(self, model) -> None:
        self.model = model
        self.gridSize = 20
        self.resetGrid()

    def resetGrid(self) -> None:
        self.cells = [[False for _ in range(self.gridSize)] for _ in range(self.gridSize)]

    def updateCell(self, x: int, y: int) -> None:
        self.cells[y][x] = not self.cells[y][x]

    def getCellNeighbourStates(self, x: int, y: int) -> list:
        neighbours = []

        for offset in self.ADJACENT:
            if (0 <= y + offset[1] < self.gridSize) and (0 <= x + offset[0] < self.gridSize):
                neighbours.append(self.cells[y + offset[1]][x + offset[0]])
            else:
                neighbours.append(False)

        return neighbours

    def updateCells(self) -> None:
        nextTick = self.cells.copy()

        for y in range(self.gridSize):
            for x in range(self.gridSize):
                neighbours = self.getCellNeighbourStates(x, y)
                cells = tf.convert_to_tensor([neighbours + [self.cells[y][x]]])
                prediction = self.model.predict(cells).flatten()[0]
                nextTick[y][x] = bool(prediction > 0.5)

        self.cells = nextTick
