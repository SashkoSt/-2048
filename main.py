import pygame
from random import randint, choice
import colors as c

WIDTH, HEIGHT = 400, 500
FPS = 30

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 Game')


class Game:
    def __init__(self, window):
        self.window = window
        self.matrix = [[0]*4 for _ in range(4)]
        self.cells = []
        self.score = [0,0]
        self.fontEngine = pygame.font.SysFont(c.SCORE_LABEL_FONT, 45)
        self.over = [False, False]
        self.startGame()
    
    def startGame(self):        
        row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2
        while self.matrix[row][col] != 0:
            row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2

        
        for i in range(1,5):
            row = []
            for j in range(4):
                rect = pygame.Rect(10+j*100, 10+i*100, 80, 80)
                textRect, textSurface = None, None
                
                if (x:=self.matrix[i-1][j]) != 0:
                    textSurface = self.fontEngine.render(str(x), True, c.CELL_NUMBER_COLORS[x])
                    textRect = textSurface.get_rect()
                    textRect.center = rect.center
                row.append({
                    "rect": rect,
                    "textRect": textRect,
                    "textSurface": textSurface
                })
            self.cells.append(row)

        scoreSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 50).render('Score : ', True, (0,0,0))
        scoreRect = scoreSurface.get_rect()
        scoreRect.top = 25
        self.score[1] = [scoreSurface, scoreRect]
def draw(window, matrix, cells, score, over):
    window.fill(c.GRID_COLOR)
    #Рахунок
    window.blit(score[1][0], score[1][1])
    scoreSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 50).render(str(score[0]), True, (0, 0, 0))
    scoreRect = scoreSurface.get_rect()
    scoreRect.top = 25
    scoreRect.left = score[1][1].right +10
    window.blit(scoreSurface, scoreRect)
    
    #Клітинки
    for i in range(4):
        for j in range(4):
            cell = cells[i][j]
            if (x:=matrix[i][j]) != 0:
                pygame.draw.rect(window, c.CELL_COLORS[x], cell['rect'])
                window.blit(cell['textSurface'], cell['textRect'])
            elif x == 0:
                pygame.draw.rect(window, c.EMPTY_CELL_COLOR, cell['rect'])
    #Закінчення гри
    if over[0] and over[1]:
        pass
    if over[0] and not over[1]:
        pass
    pygame.display.update()

def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(window)
    while running:
        clock.tick(FPS)

        draw(window, game.matrix, game.cells, game.score, game.over)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
    