import pygame
pygame.init()


def main():
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('asteroids game')
    clock = pygame.time.Clock()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        win.fill((0, 0, 0))
        pygame.draw.rect(win, (255, 0, 0), (10, 10, 50, 50))
        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()