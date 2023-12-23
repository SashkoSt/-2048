import pygame
from random import randint, choice
import colors as c

WIDTH, HEIGHT = 400, 500
FPS = 30

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 Game')

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
    