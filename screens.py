import pygame, time
from life import GameOfLife
from model import RuleModel
from widgets import Button, Text

pygame.init()

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_ALIVE = (255, 255, 255)
COLOR_RED = (128, 40, 40)
COLOR_GREEN = (40, 128, 40)

SCREEN_WIDTH = 750
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

FONT = pygame.font.SysFont(None, 24)

GRIDSIZE_UPPER_LIMIT = 200
GRIDSIZE_LOWER_LIMIT = 10

CELL_BUTTON_WIDTH = SCREEN_WIDTH / 7
OPTION_BUTTON_WIDTH = SCREEN_WIDTH / 4
OPTION_BUTTON_HEIGHT = SCREEN_WIDTH / 12

'''
RuleScreen:
- Allow drawing of new cells.
- Add drawn cells and ALIVE/DEAD as new input for ML Model.
- Continue to next Screen.
'''
class RuleScreen(RuleModel):
    def __init__(self) -> None:
        super().__init__()

        self.widgets = [
            Text("Alive", COLOR_GREEN, 50, 150, SCREEN, FONT),
            Button("", COLOR_BG, COLOR_GREEN, 45, 200, 95, 95, SCREEN, FONT, lambda : self.toggleInput()), #input state

            Button("", COLOR_BG, COLOR_GRID, 175, 100, 95, 95, SCREEN, FONT, lambda : self.toggleCell(1)),
            Button("", COLOR_BG, COLOR_GRID, 275, 100, 95, 95, SCREEN, FONT, lambda : self.toggleCell(2)),
            Button("", COLOR_BG, COLOR_GRID, 375, 100, 95, 95, SCREEN, FONT, lambda : self.toggleCell(3)),
            Button("", COLOR_BG, COLOR_GRID, 175, 200, 95, 95, SCREEN, FONT, lambda : self.toggleCell(4)),
            Button("", COLOR_BG, COLOR_GREEN, 275, 200, 95, 95, SCREEN, FONT, lambda : self.toggleInput()),
            Button("", COLOR_BG, COLOR_GRID, 375, 200, 95, 95, SCREEN, FONT, lambda : self.toggleCell(6)),
            Button("", COLOR_BG, COLOR_GRID, 175, 300, 95, 95, SCREEN, FONT, lambda : self.toggleCell(7)),
            Button("", COLOR_BG, COLOR_GRID, 275, 300, 95, 95, SCREEN, FONT, lambda : self.toggleCell(8)),
            Button("", COLOR_BG, COLOR_GRID, 375, 300, 95, 95, SCREEN, FONT, lambda : self.toggleCell(9)),

            Text("=", COLOR_ALIVE, SCREEN_WIDTH - 235, 200, SCREEN, FONT),

            Text("Dead", COLOR_RED, SCREEN_WIDTH - 115, 150, SCREEN, FONT),
            Button("", COLOR_BG, COLOR_RED, SCREEN_WIDTH - 120, 200, 95, 95, SCREEN, FONT, lambda : self.toggleOutput()), #outputstate

            Text("# of Inputs: 0", COLOR_ALIVE, SCREEN_WIDTH / 2 - 50, SCREEN_WIDTH / 10 * 7, SCREEN, FONT),
            Button("Input State", COLOR_ALIVE, COLOR_GRID, SCREEN_WIDTH / 8, SCREEN_WIDTH / 5 * 4, SCREEN_WIDTH / 4, 50, SCREEN, FONT, lambda : self.addInput()), 
            Button("Clear State", COLOR_ALIVE, COLOR_GRID, SCREEN_WIDTH / 8 * 3.5, SCREEN_WIDTH / 5 * 4, SCREEN_WIDTH / 4, 50, SCREEN, FONT, lambda : self.clearInput()), #options
            Button(" Play Game ", COLOR_ALIVE, COLOR_GRID, SCREEN_WIDTH / 8 * 6, SCREEN_WIDTH / 5 * 4, SCREEN_WIDTH / 4, 50, SCREEN, FONT, lambda : self.goToGame()),

            Text("**If no inputs are added, standard rules will be used.**", COLOR_ALIVE, SCREEN_WIDTH / 2 - 200, SCREEN_WIDTH / 10 * 9, SCREEN, FONT)
        ]

        self.engineLoop()


    def updateScreen(self) -> None:
        SCREEN.fill(COLOR_BG)

        for widget in self.widgets:
            widget.draw()


    def engineLoop(self) -> None:
        self.running = True
        self.auto_quit = False
        while self.running:
            self.updateScreen()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.auto_quit:
                    if self.inputs:
                        self.train_model()
                    return
            
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()

                    for widget in self.widgets:
                        if type(widget) == Button:
                            widget.process(pos)
    
    
    def toggleInput(self) -> None:
        ALIVE = COLOR_GREEN
        DEAD = COLOR_RED

        if self.widgets[0].text == "Alive":
            self.widgets[0].text = "Dead"
            self.widgets[0].color = DEAD
            self.widgets[1].color_bg = DEAD
            self.widgets[6].color_bg = DEAD
        else:
            self.widgets[0].text = "Alive"
            self.widgets[0].color = ALIVE
            self.widgets[1].color_bg = ALIVE
            self.widgets[6].color_bg = ALIVE


    def toggleOutput(self) -> None:
        ALIVE = COLOR_GREEN
        DEAD = COLOR_RED

        if self.widgets[12].text == "Alive":
            self.widgets[12].text = "Dead"
            self.widgets[12].color = DEAD
            self.widgets[13].color_bg = DEAD
        else:
            self.widgets[12].text = "Alive"
            self.widgets[12].color = ALIVE
            self.widgets[13].color_bg = ALIVE
    

    def toggleCell(self, index) -> None:
        ON = COLOR_ALIVE
        OFF = COLOR_GRID
        INDEX = index + 1

        if self.widgets[INDEX].color_bg == ON:
            self.widgets[INDEX].color_bg = OFF
        else:
            self.widgets[INDEX].color_bg = ON
    

    def addInput(self):
        input = False
        if self.widgets[0].text == "Alive":
            input = True

        cells = []
        for i in range(2, 11):
            if i == 6:
                continue

            if self.widgets[i].color_bg == COLOR_ALIVE:
                cells.append(True)
            else:
                cells.append(False)

        output = False
        if self.widgets[12].text == "Alive":
            output = True

        self.add_state(input, cells, output)
        self.widgets[14].text = f"# of Inputs: {len(self.inputs)}"
    

    def clearInput(self):
        for i in range(2, 11):
            if self.widgets[i].color_bg == COLOR_ALIVE:
                self.toggleCell(i-1)


    def goToGame(self):
        self.auto_quit = True
                    
                

'''
GameScreen:
- Allow drawing of new cells.
- Continue / Pause generations.
- Draw given cells as alive.
- Check minimum length needed to show all cells.
'''
class GameScreen(GameOfLife):
    def __init__(self, ruleset: list) -> None:
        super().__init__(ruleset)
        self.gridSize = 20
        self.engineLoop()


    def updateScreen(self) -> None:
        self.cellSize = SCREEN_WIDTH / self.gridSize

        pygame.draw.rect(SCREEN, COLOR_GRID, (0, 0, SCREEN_WIDTH, SCREEN_WIDTH))
        for row in range(0, self.gridSize):
            for col in range(0, self.gridSize):
                color = COLOR_ALIVE if (row in self.cells and col in self.cells[row]) else COLOR_BG
                pygame.draw.rect(SCREEN, color, (col * self.cellSize, row * self.cellSize, self.cellSize - 1, self.cellSize - 1))


    def changeZoom(self, change: int) -> None:
        self.gridSize -= change * 2

        if self.gridSize > GRIDSIZE_UPPER_LIMIT:
            self.gridSize = GRIDSIZE_UPPER_LIMIT

        elif self.gridSize < GRIDSIZE_LOWER_LIMIT:
            self.gridSize = GRIDSIZE_LOWER_LIMIT

    
    def advanceOneState(self):
        self.updateCells()
        self.updateScreen()
        pygame.display.update()


    def engineLoop(self) -> None:
        running = False
        while True:
            self.updateScreen()
            pygame.display.update()

            if running:
                self.updateCells()
                time.sleep(1 / self.gridSize)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = not running
                    elif event.key == pygame.K_r:
                        self.resetGrid()
                    elif event.key == pygame.K_o:
                        self.advanceOneState()
                        
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    self.addCell(pos[0] // self.cellSize, pos[1] // self.cellSize)
                
                if event.type == pygame.MOUSEWHEEL:
                    self.changeZoom(event.y)

