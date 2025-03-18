import pygame, time

from .life import GameOfLife

pygame.init()

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_ALIVE = (255, 255, 255)
COLOR_RED = (128, 40, 40)
COLOR_GREEN = (40, 128, 40)

SCREEN_WIDTH = 750
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

FONT = pygame.font.SysFont(None, 24)

CELL_BUTTON_WIDTH = SCREEN_WIDTH / 7
OPTION_BUTTON_WIDTH = SCREEN_WIDTH / 4
OPTION_BUTTON_HEIGHT = SCREEN_WIDTH / 12


class GameScreen(GameOfLife):
    def __init__(self, model) -> None:
        super().__init__(model)
        self.gridSize = 20
        self.engineLoop()


    def updateScreen(self) -> None:
        self.cellSize = SCREEN_WIDTH / self.gridSize

        pygame.draw.rect(SCREEN, COLOR_GRID, (0, 0, SCREEN_WIDTH, SCREEN_WIDTH))
        for row in range(0, self.gridSize):
            for col in range(0, self.gridSize):
                color = COLOR_ALIVE if (row in self.cells and col in self.cells[row]) else COLOR_BG
                pygame.draw.rect(SCREEN, color, (col * self.cellSize, row * self.cellSize, self.cellSize - 1, self.cellSize - 1))

    
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

