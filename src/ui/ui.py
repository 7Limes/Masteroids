from typing import Callable
import pygame
from pygame import Vector2, Surface


ICON_SIZE = 64
VERTICAL_PADDING = 10


class UpgradeBox:
    def __init__(self, icon: Surface, title: str, cost: int, level: int, callback: Callable):
        self.icon = pygame.transform.scale(icon, (ICON_SIZE, ICON_SIZE))
        self.title = title
        self.cost = cost
        self.level = level
        self.callback = callback

        self.position: Vector2 = Vector2(0, 0)
        self.size: Vector2 = Vector2(0, 0)

        self.hovered = False


    def get_surface(self, font: pygame.font.Font, size: Vector2) -> Surface:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((0, 0, 0, 64))
        surf.blit(self.icon, (5, 5))

        title_label = font.render(self.title, True, (255, 255, 255, 255))
        icon_width = self.icon.get_size()[0]
        surf.blit(title_label, (icon_width + 10, 5))

        cost_label = font.render(f'Cost: {self.cost} coins', True, (255, 255, 255, 255))
        surf.blit(cost_label, (icon_width + 10, 25))

        level_label = font.render(f'Current Level: {self.level}', True, (255, 255, 255, 255))
        surf.blit(level_label, (icon_width + 10, 45))

        if self.hovered:
            pygame.draw.rect(surf, (255, 255, 255, 255), (0, 0, size.x, size.y), 3)
        return surf


    def hits_point(self, point: Vector2):
        return (point.x > self.position.x and point.x < self.position.x+self.size.x and
                point.y > self.position.y and point.y < self.position.y+self.size.y)


class UiHandler:
    def __init__(self, elements: list):
        self.elements: list = elements
        self.selected_element = None
        self.prev_lmb_state = False


    def update(self):
        lmb_state = pygame.mouse.get_pressed()[0]
        mouse_position = Vector2(pygame.mouse.get_pos())
        for element in self.elements:
            if element.hits_point(mouse_position):
                self.selected_element = element
                element.hovered = True
            else:
                element.hovered = False
        if all(not e.hovered for e in self.elements):
            self.selected_element = None
        
        if not self.prev_lmb_state and lmb_state:
            if self.selected_element is not None:
                self.selected_element.callback()
        self.prev_lmb_state = lmb_state
    

    def clear(self):
        self.elements.clear()


    def draw(self, surf: Surface, font: pygame.font.Font):
        surf_width, surf_height = surf.get_size()
        box_width = max(surf_width / 4, 400)
        box_height = max(surf_height / 2 / len(self.elements), 80)
        box_x = surf_width / 2 - box_width / 2
        for i, element in enumerate(self.elements):
            box_y =  i * (box_height + VERTICAL_PADDING) + 30
            box_surf: Surface = element.get_surface(font, Vector2(box_width, box_height))
            surf.blit(box_surf, (box_x, box_y))
            element.position = Vector2(box_x, box_y)
            element.size = Vector2(box_width, box_height)