import pygame
import sys
import pygame.font

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAVITY = 0.5

# Initialize Pygame
pygame.init()


# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")

# Clock to control frame rate
clock = pygame.time.Clock()

#font object
font = pygame.font.SysFont(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create player's surface (sprite) and set initial position
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        #self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.rect = self.image.get_rect(bottomleft=(10, SCREEN_HEIGHT))
        # Player's movement speed
        self.speed = 5

        #VERTICAL VELOCITY OF PLAYER FOR JUMPING
        self.velocity_y = 0

        self.health = 100
        self.score = 0

        #maximum jump height
        self.jump_height = -10

        #health
        self.max_health = 100
        self.health = self.max_health

        #defining health derease amount when hit by enemy
        self.damage_amount = 10 

        self.invincible = False


        #storing previous position for jump detection
        self.prev_bottom = self.rect.bottom

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

        #keeping player within boundary

       if self.rect.left < 0:
            self.rect.left = 0
       if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH  
       
        #update previous bottom position
       self.prev_bottom = self.rect.bottom

    def jump(self):
         # Check if the player is on the ground before jumping
        if self.rect.bottom == SCREEN_HEIGHT:
            self.velocity_y = self.jump_height  
        

    def handle_collision(self, enemy):
         if not self.invincible:
             self.health -=10
             #setting player invincible after being hit
             self.invincible = True
             pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    def draw_health_bar(self, surface):
        # Calculate the width of the health bar
        bar_width = int(self.rect.width * (self.health / self.max_health))
        # Create the health bar surface
        health_bar = pygame.Surface((bar_width, 10))
        if self.health > 60:
            color = GREEN
        elif self.health > 30:
            color = YELLOW
        else:
            color = RED
        health_bar.fill(color)
        # Draw the health bar above the player's sprite
        surface.blit(health_bar, (self.rect.x, self.rect.y - 20))



# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red color for enemy
        #self.rect = self.image.get_rect()

        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.speed = 3  # Adjust speed as needed


        self.max_health= 50
        self.health = self.max_health
    def update(self):
        # Implement enemy movement logic here
        self.rect.x -= self.speed

        #make enemy only move within window
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH


    def draw_health_bar(self, surface):
        # Calculate the width of the health bar
        bar_width = int(self.rect.width * (self.health / self.max_health))
        # Create the health bar surface
        health_bar = pygame.Surface((bar_width, 5))
        health_bar.fill(RED)  # You can customize the color for enemies
        # Draw the health bar above the enemy's sprite
        surface.blit(health_bar, (self.rect.x, self.rect.y - 10))  
    

# Main game loop
def main():
    # Create player object
    player = Player()
    
    #enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT // 2)
    enemy = Enemy(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 30)

    # Create sprite group for all game objects
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, enemy)


    # Main loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            # Check if user quits the game
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.USEREVENT:
                player.invincible = False

        # Game logic
        all_sprites.update()
        
       
        #checking collissions
        collissions = pygame.sprite.spritecollide(player, [enemy], False)
        for enemy_hit in collissions:
            player.handle_collision(enemy_hit)      

        
        # Rendering
        # Clear the screen
        screen.fill(BLACK)
        # Draw all sprites onto the screen
        all_sprites.draw(screen)

        # Draw health bars for player and enemy
        player.draw_health_bar(screen)
        enemy.draw_health_bar(screen)


         #Render score text
        score_text = font.render("Score: "+str(player.score), True, WHITE)
        #Blit score text onto screen
        screen.blit(score_text, (50, 50))
        
        # Flip the display
        pygame.display.flip()
        # Cap the frame rate at 60 FPS
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
