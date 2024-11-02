import pygame

pygame.init()
pygame.mixer.init()

from player import Player
from resource_manager import ResourceManager
from hazards.asteroid import Asteroid


def load_resources(resource_manager: ResourceManager):
    resource_manager.load_image('player', 'assets/temp-player.png')
    resource_manager.load_image('asteroid', 'assets/temp-asteroid.png')


def draw_debug_label(surf: pygame.Surface, font: pygame.font.Font, text: str, position: tuple[int, int]):
    surf.blit(font.render(text, True, (255, 255, 255)), position)


def main():
    win = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE)
    pygame.display.set_caption('asteroids game')
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('Arial', 15)

    resource_manager = ResourceManager()
    load_resources(resource_manager)

    player = Player()
    asteroids = [
        Asteroid(pygame.Vector2(20, 20), 5, pygame.Vector2(-1, -0.5)),
        Asteroid(pygame.Vector2(15, -10), 4, pygame.Vector2(-2, 1))
    ]

    delta: float = 0.0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()

        player.handle_input(delta, keys)
        player.update(delta)


        win.fill((0, 0, 0))

        player.draw(win, resource_manager)
        for a in asteroids:
            a.update(delta)
            a.draw(win, player.position, resource_manager)

        draw_debug_label(win, font, f'fps: {clock.get_fps():.1f}', (0, 0))
        draw_debug_label(win, font, f'pos: {player.position}', (0, 20))
        draw_debug_label(win, font, f'vel: {player.velocity}', (0, 40))
        draw_debug_label(win, font, f'angle: {player.angle:.1f}', (0, 60))


        delta = clock.tick(60) / 1000.0
        pygame.display.flip()


if __name__ == '__main__':
    main()