from typing import Callable
import pygame
from pygame import Vector2, Surface


ICON_SIZE = 80
VERTICAL_PADDING = 10



class Button:
    def __init__(self, position: Vector2, size: Vector2, callback: Callable):
        self.position = position
        self.size = size
        self.callback = callback

        self.hovered = False
    
    def update_position_size(self, position: Vector2, size: Vector2):
        self.position = position
        self.size = size
    
    def hits_point(self, point: Vector2):
        return (point.x > self.position.x and point.x < self.position.x+self.size.x and
                point.y > self.position.y and point.y < self.position.y+self.size.y)

    def get_surface(self) -> Surface:
        surf = pygame.Surface(self.size, pygame.SRCALPHA)
        surf.fill((0, 0, 0, 64))
        if self.hovered:
            pygame.draw.rect(surf, (255, 255, 255, 255), (0, 0, self.size.x, self.size.y), 3)
        return surf
    
    def draw(self, surf: Surface):
        surf.blit(self.get_surface(), self.position)


class LabelButton(Button):
    def __init__(self, position: Vector2, size: Vector2, callback: Callable, text: str):
        super().__init__(position, size, callback)
        self.text = text
    
    def get_surface(self, font: pygame.font.Font) -> Surface:
        surf = super().get_surface()
        label = font.render(self.text, True, (255, 255, 255))
        label_pos = Vector2(surf.get_size()) / 2 - Vector2(label.get_size()) / 2
        surf.blit(label, label_pos)
        return surf
        

class UpgradeBox(Button):
    def __init__(self, position: Vector2, size: Vector2, callback: Callable, icon: Surface, title: str, cost: int, level: int):
        super().__init__(position, size, callback)
        self.icon = pygame.transform.scale(icon, (ICON_SIZE, ICON_SIZE))
        self.title = title
        self.cost = cost
        self.level = level

    def get_surface(self, font: pygame.font.Font) -> Surface:
        surf = super().get_surface()
        surf.blit(self.icon, (5, 5))

        title_label = font.render(self.title, True, (255, 255, 255, 255))
        icon_width = self.icon.get_size()[0]
        surf.blit(title_label, (icon_width + 10, 5))

        cost_label = font.render(f'Cost: {self.cost} coins', True, (255, 255, 255, 255))
        surf.blit(cost_label, (icon_width + 10, 25))

        level_label = font.render(f'Current Level: {self.level}', True, (255, 255, 255, 255))
        surf.blit(level_label, (icon_width + 10, 45))
        return surf


class UiHandler:
    def __init__(self, elements: list):
        self.elements: list[Button] = elements
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


    def draw(self, surf: Surface, font: pygame.font.Font, padding: int=VERTICAL_PADDING, offset: Vector2=Vector2(0, 0)):
        if not self.elements:
            return
        surf_width = surf.get_size()[0]
        for i, element in enumerate(self.elements):
            box_surf: Surface = element.get_surface(font)
            box_x = surf_width / 2 - element.size.x / 2 + offset.x
            box_y =  i * (element.size.y + VERTICAL_PADDING) + offset.y
            surf.blit(box_surf, (box_x, box_y))
            element.update_position_size(Vector2(box_x, box_y), element.size)