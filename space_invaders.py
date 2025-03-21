"""
Space Invaders Game
------------------
A classic Space Invaders game implementation using Pygame.
This game features a player-controlled spaceship that must defend against
invading aliens. The player can move left and right, and shoot bullets
to destroy the enemies before they reach the bottom of the screen.

Author: Theo Goncalves
Version: 1.0.0
Date: 2024
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800      # Width of the game window in pixels
SCREEN_HEIGHT = 600     # Height of the game window in pixels
PLAYER_SPEED = 5        # Speed at which the player moves
BULLET_SPEED = 7        # Speed at which bullets travel
ENEMY_SPEED = 2         # Speed at which enemies move horizontally
ENEMY_DROP = 40         # Distance enemies drop when reaching screen edge

# Color Definitions (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the game window and initialize game clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    """
    Player class representing the player's spaceship.
    
    Attributes:
        image (Surface): The visual representation of the player
        rect (Rect): The rectangular area occupied by the player
        speed (int): The movement speed of the player
    """
    
    def __init__(self):
        """Initialize the player sprite with default position and properties."""
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2  # Center horizontally
        self.rect.bottom = SCREEN_HEIGHT - 10  # Position near bottom
        self.speed = PLAYER_SPEED

    def update(self):
        """
        Update the player's position based on keyboard input.
        Player can move left and right using arrow keys.
        Movement is constrained to the screen boundaries.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    """
    Bullet class representing projectiles shot by the player.
    
    Attributes:
        image (Surface): The visual representation of the bullet
        rect (Rect): The rectangular area occupied by the bullet
        speed (int): The movement speed of the bullet
    """
    
    def __init__(self, x, y):
        """
        Initialize a bullet at the specified position.
        
        Args:
            x (int): The x-coordinate where the bullet starts
            y (int): The y-coordinate where the bullet starts
        """
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED

    def update(self):
        """
        Update the bullet's position.
        Bullets move upward and are removed when they leave the screen.
        """
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    """
    Enemy class representing the invading aliens.
    
    Attributes:
        image (Surface): The visual representation of the enemy
        rect (Rect): The rectangular area occupied by the enemy
        direction (int): The direction of movement (1 for right, -1 for left)
    """
    
    def __init__(self, x, y):
        """
        Initialize an enemy at the specified position.
        
        Args:
            x (int): The x-coordinate where the enemy starts
            y (int): The y-coordinate where the enemy starts
        """
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # Start moving right

    def update(self):
        """
        Update the enemy's position.
        Enemies move horizontally based on their direction.
        """
        self.rect.x += ENEMY_SPEED * self.direction

# Create sprite groups for managing game objects
all_sprites = pygame.sprite.Group()  # Contains all game sprites
enemies = pygame.sprite.Group()      # Contains only enemy sprites
bullets = pygame.sprite.Group()      # Contains only bullet sprites
player = Player()                    # Create the player

# Add player to the all_sprites group
all_sprites.add(player)

# Create the initial formation of enemies
for row in range(5):
    for column in range(8):
        enemy = Enemy(column * 80 + 100, row * 60 + 50)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create and add a new bullet when spacebar is pressed
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update all sprites
    all_sprites.update()

    # Check if enemies need to change direction
    for enemy in enemies:
        if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
            # Reverse direction and move down for all enemies
            for e in enemies:
                e.direction *= -1
                e.rect.y += ENEMY_DROP
            break

    # Check for collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the framerate at 60 FPS
    clock.tick(60)

# Clean up and exit
pygame.quit()
sys.exit()