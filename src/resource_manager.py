import pygame
from pygame import mixer

class ResourceManager:
    def __init__(self):
        self.images: dict[str, pygame.Surface] = {}
        self.sounds: dict[str, mixer.Sound] = {}
    
    def load_image(self, name: str, image_path: str):
        img = pygame.image.load(image_path).convert_alpha()
        self.images[name] = img
    
    def load_sound(self, name: str, sound_path: str):
        sound = mixer.Sound(sound_path)
        self.sounds[name] = sound
    
    def get_image(self, name: str) -> pygame.Surface:
        return self.images[name]

    def get_sound(self, name: str) -> mixer.Sound:
        return self.sounds[name]