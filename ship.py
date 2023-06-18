import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the game and set it's starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get it's rect.
        self.image = pygame.image.load(
            'Project/alien_invasion_8/image/ufo.bmp')
        DEFAULT_IMAGE_SIZE = (100, 100)
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        # self.image =pygame.transform.rotate(self.image,60)
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizental position
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at the current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the flag's movement"""
        # update the ship's x value,not the rect
        # limiting the ship's range
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # update rect object from self.x
        self.rect.x = self.x
        
    def center_ship(self):
        """Center the ship of the screen"""
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
