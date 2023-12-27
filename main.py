import pygame  # Імпорт бібліотеки Pygame для створення гри
from random import randint, choice  # Імпорт функцій randint і choice для випадкових чисел та випадкового вибору
import colors as c  # Імпорт модулю colors для визначення кольорів

WIDTH, HEIGHT = 400, 500  # Задання ширини та висоти вікна гри
FPS = 30  # Задання кадрової частоти гри

pygame.init()  # Ініціалізація Pygame
window = pygame.display.set_mode((WIDTH, HEIGHT))  # Створення вікна гри
pygame.display.set_caption('2048 Game')  # Задання заголовку вікна гри

# Клас гри
class Game:
    def __init__(self, window):
        self.window = window
        self.matrix = [[0]*4 for _ in range(4)]  # Ініціалізація матриці 4x4 для представлення стану гри
        self.cells = []  # Список клітинок на ігровому полі
        self.score = [0, 0]  # Рахунок гравця та виведений на екран
        self.fontEngine = pygame.font.SysFont(c.SCORE_LABEL_FONT, 45)  # Шрифт для виведення рахунку на екран
        self.over = [False, False]  # Прапорці для визначення закінчення гри
        self.startGame()  # Метод для початку гри

    def startGame(self):
        # Генерація двох початкових плиток з числами 2        
        row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2
        while self.matrix[row][col] != 0:
            row, col = randint(0,3), randint(0,3)
        self.matrix[row][col] = 2

        # Створення клітинок та їх розміщення на ігровому полі
        for i in range(1,5):
            row = []
            for j in range(4):
                rect = pygame.Rect(10+j*100, 10+i*100, 80, 80)
                textRect, textSurface = None, None
                # Відображення числа на клітинці, якщо воно не дорівнює 0
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
        # Відображення рахунку на екрані
        scoreSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 50).render('Score : ', True, (0,0,0))
        scoreRect = scoreSurface.get_rect()
        scoreRect.top = 25
        self.score[1] = [scoreSurface, scoreRect]
    def addNewTile(self):
        row, col = randint(0,3), randint(0,3)# Генеруємо випадкові координати (рядок і стовпець) для нової плитки
        # Перевіряємо, чи на випадкових координатах вже є плитка (не нуль)
        while self.matrix[row][col] != 0:
            # Якщо так, генеруємо нові випадкові координати
            row, col = randint(0,3), randint(0,3)
        # Встановлюємо на вибраних координатах нову плитку зі значенням 2 або 4
        self.matrix[row][col] = choice([2,2,2,2,4])
    def Hor_Move(self):
        # Перевіряємо, чи є можливість руху горизонтально
        for i in range(4):
            for j in range(3):
                # Перевіряємо, чи існують дві сусідні плитки з однаковими значеннями в ряду
                if self.matrix[i][j+1] == self.matrix[i][j]:
                    return True # Якщо так, повертаємо True, щоб позначити можливість руху
        return False # Якщо не знайдено пар однакових сусідніх плиток, повертаємо False
    def Ver_Move(self):
        # Перевіряємо, чи є можливість руху вертикально
        for i in range(3):
            for j in range(4):
                # Перевіряємо, чи існують дві сусідні плитки з однаковими значеннями в стовпці
                if self.matrix[i+1][j] == self.matrix[i][j]:
                    # Якщо так, повертаємо True, щоб позначити можливість руху
                    return True
        # Якщо не знайдено пар однакових сусідніх плиток, повертаємо False
        return False
    
    def gameOver(self):
        # Перевіряємо, чи гравець досягнув значення 2048 в будь-якому рядку матриці
        if any(2048 in row for row in self.matrix):
            self.over = [True, True]# Якщо так, гра закінчена і гравець виграв
        # Перевіряємо, чи не залишилося жодного вільного місця в матриці і чи немає можливих рухів
        if not any(0 in row for row in self.matrix) and not self.Hor_Move() and not self.Ver_Move():
            self.over = [True, False]# Якщо так, гра закінчена і гравець програв

    def updateTiles(self):
        # Оновлюємо тексти на плитках відповідно до значень у матриці
        for i in range(4):
            for j in range(4):
                # Якщо значення не нуль, оновлюємо текст і відображення на плитці
                if (x:=self.matrix[i][j]) != 0:
                    # Створюємо текст зі значенням плитки та відповідним кольором
                    textSurface = self.fontEngine.render(str(x), True, c.CELL_NUMBER_COLORS[x])
                    # Визначаємо прямокутник текстової поверхні та центруємо його в середині плитки
                    textRect = textSurface.get_rect()
                    textRect.center = self.cells[i][j]['rect'].center
                    # Оновлюємо інформацію про текст на плитці
                    self.cells[i][j]['textRect'] = textRect
                    self.cells[i][j]['textSurface'] = textSurface
                # Якщо значення нуль, видаляємо тексти з плитки
                elif x == 0:
                    self.cells[i][j]['textRect'] = None
                    self.cells[i][j]['textSurface'] = None

    def stack(self):
        new_matrix = [[0]*4 for _ in range(4)]# Створюємо нову матрицю, щоб зберегти результуючий стан плиток після операції "stack"
        # Здійснюємо операцію "stack" для кожного рядка матриці
        for i in range(4):
            position = 0# Позначає поточну позицію для вставки значень в новий рядок
            for j in range(4):
                # Якщо значення плитки не нуль, вставляємо його на наступну доступну позицію
                if self.matrix[i][j] != 0:
                    new_matrix[i][position] = self.matrix[i][j]
                    position += 1
        # Оновлюємо матрицю гри новим станом плиток            
        self.matrix = new_matrix
    
    def combine(self):
        # Об'єднання сусідніх плиток з однаковими значеннями у рядках
        for i in range(4): 
            for j in range(3):
                x = self.matrix[i][j]
                # Якщо поточна плитка не нуль і її значення рівне значенню сусідньої плитки
                if x != 0 and x == self.matrix[i][j+1]:
                    # Збільшуємо значення поточної плитки удвічі
                    self.matrix[i][j] *= 2
                    # Значення сусідньої плитки стає нулем
                    self.matrix[i][j+1] = 0
                    # Збільшуємо рахунок гравця на значення нової плитки
                    self.score[0] += self.matrix[i][j]
        
    def reverse(self):
        # Відображення кожного рядка матриці гри (реверс)
        new_matrix = []
        for row in self.matrix:
            new_matrix.append(row[::-1])
        # Оновлюємо матрицю гри з відображеними рядками
        self.matrix = new_matrix
    
    def transpose(self):
        # Транспонування матриці гри (обмін рядків і стовпців)
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[j][i] = self.matrix[i][j]
        # Оновлюємо матрицю гри транспонованою матрицею
        self.matrix = new_matrix
    
    def scs(self):
        # Зберігаємо стан матриці перед виконанням операцій stack, combine і stack
        oldmatrix = self.matrix
        # Виконуємо операції stack, combine, stack
        self.stack()
        self.combine()
        self.stack()
        # Повертаємо старий стан матриці
        return oldmatrix

    def aug(self):
        # Додаємо нову плитку, оновлюємо тексти на плитках і перевіряємо, чи гра завершилася
        self.addNewTile()
        self.updateTiles()
        self.gameOver()

    def left(self):
        oldmatrix = self.scs()# Виконує лівий рух у грі
        # Якщо після операції scs стан матриці не змінився, вихід
        if oldmatrix == self.matrix:
            return
        # Виконує операцію aug для додавання нової плитки та перевірки закінчення гри
        self.aug()
    
    def right(self):
        # Виконує правий рух у грі
        oldmatrix = self.matrix
        # Відображає матрицю, виконує операції scs та відображає матрицю назад
        self.reverse()
        self.scs()
        self.reverse()
        # Якщо після операції scs стан матриці не змінився, вихід
        if oldmatrix == self.matrix:
            return
        # Виконує операцію aug для додавання нової плитки та перевірки закінчення гри
        self.aug()
    
    def up(self):
        # Виконує верхній рух у грі
        oldmatrix = self.matrix
        # Транспонує матрицю, виконує операції scs та транспонує матрицю назад
        self.transpose()
        self.scs()
        self.transpose()
        # Якщо після операції scs стан матриці не змінився, вихід
        if oldmatrix == self.matrix:
            return
        # Виконує операцію aug для додавання нової плитки та перевірки закінчення гри
        self.aug()

    def down(self):
        # Виконує нижній рух у грі
        oldmatrix = self.matrix
        # Транспонує матрицю, відображає та виконує операції scs та транспонує матрицю назад
        self.transpose()
        self.reverse()
        self.scs()
        self.reverse()
        self.transpose()
        # Якщо після операції scs стан матриці не змінився, вихід
        if oldmatrix == self.matrix:
            return
        # Виконує операцію aug для додавання нової плитки та перевірки закінчення гри
        self.aug()
    
    def reset(self):
        # Скидає гру в початковий стан
        self.__init__(self.window)

def draw(window, matrix, cells, score, over):
    # Очищення вікна та встановлення кольору
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
                # Вивід заповненої клітинки з текстом
                pygame.draw.rect(window, c.CELL_COLORS[x], cell['rect'])
                window.blit(cell['textSurface'], cell['textRect'])
            elif x == 0:
                # Вивід порожньої клітинки
                pygame.draw.rect(window, c.EMPTY_CELL_COLOR, cell['rect'])
    #Закінчення гри
    if over[0] and over[1]:
        # Вивід повідомлення, якщо гра пройдена
        gameOverSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 20).render('               Гру пройдено!. \nНатисніть Ctrl + q, щоб почати знову', True, (0,0,0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH//2, HEIGHT//2)
        window.blit(gameOverSurface, gameOverRect)
        # Вивід повідомлення, якщо гравець програв
    if over[0] and not over[1]:
        gameOverSurface = pygame.font.SysFont(c.SCORE_LABEL_FONT, 20).render('               Ви програли. \nНатисніть Ctrl + q, щоб почати знову', True, (0,0,0))
        gameOverRect = gameOverSurface.get_rect()
        gameOverRect.center = (WIDTH//2, HEIGHT//2)
        window.blit(gameOverSurface, gameOverRect)

    pygame.display.update()# Оновлення вікна

def main():
    # Ініціалізація гри та змінних
    running = True
    clock = pygame.time.Clock()
    game = Game(window)

    # Головний цикл гри
    while running:
        clock.tick(FPS)

        draw(window, game.matrix, game.cells, game.score, game.over)# Вивід графічного представлення гри на екран
        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.left()
                if event.key == pygame.K_RIGHT:
                    game.right()
                if event.key == pygame.K_UP:
                    game.up()
                if event.key == pygame.K_DOWN:
                    game.down()
                # Обробка комбінації Ctrl + q для скидання гри, якщо гра завершена
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL and game.over:
                    game.reset()
    # Завершення гри
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
    