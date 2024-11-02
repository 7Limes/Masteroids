import random
import pygame
from pygame import mixer, Surface

class ResourceManager:
    def __init__(self):
        self.images: dict[str, Surface] = {}
        self.spritesheets: dict[str, list[Surface]] = {}
        self.sounds: dict[str, mixer.Sound] = {}
    
    def load_image(self, image_id: str, image_path: str):
        img = pygame.image.load(image_path).convert_alpha()
        self.images[image_id] = img
    
    def load_spritesheet(self, spritesheet_id: str, spritesheet_path: str):
        sheet_images: list[Surface] = []
        sheet = pygame.image.load(spritesheet_path).convert_alpha()

        sprite_size, spritesheet_height = sheet.get_size()
        amount_sprites = spritesheet_height // sprite_size
        for i in range(amount_sprites):
            sprite = Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), (0, i*sprite_size, sprite_size, sprite_size))
            sheet_images.append(sprite)
        
        self.spritesheets[spritesheet_id] = sheet_images
    
    def load_sound(self, sound_id: str, sound_path: str):
        sound = mixer.Sound(sound_path)
        self.sounds[sound_id] = sound
    

    def get_image(self, image_id: str) -> Surface:
        return self.images[image_id]

    def get_full_spritesheet(self, spritesheet_id: str) -> list[Surface]:
        return self.spritesheets[spritesheet_id]

    def get_spritesheet_image(self, spritesheet_id: str, index: int) -> Surface:
        return self.spritesheets[spritesheet_id][index]
    
    def get_random_spritesheet_image(self, name: str) -> Surface:
        return random.choice(self.spritesheets[name])

    def get_sound(self, sound_id: str) -> mixer.Sound:
        return self.sounds[sound_id]