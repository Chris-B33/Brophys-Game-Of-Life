import tensorflow as tf

class GameOfLife:
    ADJACENT = (
        (-1,-1), (0,-1), (1,-1),
        (-1, 0),         (1, 0),
        (-1, 1), (0, 1), (1, 1)
    )


    def __init__(self, model) -> None:
        self.model = model
        self.resetGrid()


    def resetGrid(self) -> None:
        self.cells = {}


    def addCell(self, x: int, y: int) -> None:
        if y not in self.cells:
            self.cells[y] = set([x])
            
        elif x not in self.cells[y]:
            self.cells[y].add(x)


    def delCell(self, x: int, y: int) -> None:
        if (y in self.cells and x in self.cells[y]):
            self.cells[y].remove(x)
 
            if not self.cells[y]:
                del self.cells[y]


    def getAliveAndAdjacentCells(self) -> set:
        all_coordinates = set()

        for y in self.cells:
            for x in self.cells[y]:                
                for i in self.ADJACENT:
                    c = (x + i[0], y + i[1])                        
                    all_coordinates.add(c)

        return all_coordinates
    

    def getCellNeighbourStates(self, x: int, y: int) -> list:
        neighbours = []

        for i in self.ADJACENT:
            if y + i[1] in self.cells and x + i[0] in self.cells[y + i[1]]:
                neighbours.append(True)
            else:
                neighbours.append(False)

        return neighbours


    def updateCells(self) -> None:
        nextTick = {}

        for cell in self.getAliveAndAdjacentCells():
            x = cell[0]
            y = cell[1]
            alive = True if y in self.cells and x in self.cells[y] else False
            neighbours = self.getCellNeighbourStates(x, y)

            cells = tf.convert_to_tensor([neighbours + [alive]])

            if self.model.predict(cells):
                if y not in nextTick:
                    nextTick[y] = set([x])
    
                elif x not in nextTick[y]:
                    nextTick[y].add(x)

        self.cells = nextTick
