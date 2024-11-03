import pygame
import random
from pygame.math import Vector2
import util


class StarfieldBackground:
    def __init__(self, initial_size, num_stars=1000, parallax_factor=0.5):
        """
        Initialize the starfield background
        
        Args:
            initial_size (tuple): Initial size of the surface (width, height)
            num_stars (int): Number of stars to generate
            parallax_factor (float): How much slower the stars move compared to the foreground
                                   (0 = static, 1 = moves with foreground)
        """
        self.width, self.height = initial_size
        self.num_stars = num_stars
        self.parallax_factor = parallax_factor
        self.surface = pygame.Surface(initial_size)
        
        # Generate random star positions
        # We generate them in a larger area than the screen to allow for movement
        self.stars = []
        padding = 1000  # Extra space around the visible area
        for _ in range(num_stars):
            x = random.uniform(-padding, self.width + padding)
            y = random.uniform(-padding, self.height + padding)
            radius = random.randint(1, 2)  # Random star size
            self.stars.append((Vector2(x, y), radius))
    
    def resize(self, new_size):
        """Resize the background surface"""
        self.width, self.height = new_size
        self.surface = pygame.Surface(new_size)
    
    def update(self, player_pos):
        """
        Update the starfield based on player position
        
        Args:
            player_pos (Vector2): Current player position
        """
        # Clear the surface
        self.surface.fill((0, 0, 0))  # Black background
        
        # Calculate offset based on player position and parallax factor
        offset = player_pos * self.parallax_factor
        
        # Draw each star
        for star_pos, radius in self.stars:
            # Calculate screen position
            screen_pos = star_pos - offset
            
            # Wrap stars around the screen
            wrapped_x = screen_pos.x % (self.width + 200) - 100
            wrapped_y = screen_pos.y % (self.height + 200) - 100
            
            # Only draw if within screen bounds (with some padding)
            color = util.interpolate_color((64, 64, 64), (128, 128, 128), random.uniform(0, 1))
            if (-100 <= wrapped_x <= self.width + 100 and 
                -100 <= wrapped_y <= self.height + 100):
                pygame.draw.circle(
                    self.surface,
                    color,
                    (wrapped_x, wrapped_y),
                    radius
                )
    
    def draw(self, target_surface):
        """Draw the starfield to the target surface"""
        target_surface.blit(self.surface, (0, 0))
