import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.5

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

        #VERTICAL VELOCITY OF PLAYER FOR JUMPING
        self.velocity_y = 0

        #maximum jump height
        self.jump_height = -10

    def update(self):
       self.velocity_y +=GRAVITY
       self.rect.y += self.velocity_y

       if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
       
       
        # Update player's position based on keyboard input
       keys = pygame.key.get_pressed()
       if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
       if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
       if keys[pygame.K_SPACE]:
            self.jump()    


    def jump(self):
 # Check if the player is on the ground before jumping
        if self.rect.bottom == SCREEN_HEIGHT:
            self.velocity_y = self.jump_height  


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red color for enemy
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3  # Adjust speed as needed

    def update(self):
        # Implement enemy movement logic here
        self.rect.x -= self.speed

        #make enemy only move within window
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

# Main game loop
def main():
    # Create player object
    player = Player()

    # Create sprite group for all game objects
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    #create sprite group for enemies
    enemies = pygame.sprite.Group()

    #addding enemies to group
    enemy1 = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT // 2)
    enemies.add(enemy1)
    all_sprites.add(enemy1)

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
