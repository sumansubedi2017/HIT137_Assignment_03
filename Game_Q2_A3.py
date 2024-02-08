import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")

# Clock to control frame rate
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create player's surface (sprite) and set initial position
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        # Player's movement speed
        self.speed = 5

    def update(self):
        # Update player's position based on keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

# Main game loop
def main():
    # Create player object
    player = Player()

    # Create sprite group for all game objects
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Main loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            # Check if user quits the game
            if event.type == pygame.QUIT:
                running = False

        # Game logic
        all_sprites.update()

        # Rendering
        # Clear the screen
        screen.fill(BLACK)
        # Draw all sprites onto the screen
        all_sprites.draw(screen)
        # Flip the display
        pygame.display.flip()
        # Cap the frame rate at 60 FPS
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()