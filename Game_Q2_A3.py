import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 50
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 5
COLLECTIBLE_WIDTH = 30
COLLECTIBLE_HEIGHT = 30

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
import os

# Get the current working directory
current_directory = os.getcwd()
print("Current working directory:", current_directory)


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        #self.image.fill(RED)
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        scale_factor = 2  # Adjust as needed
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH * scale_factor, PLAYER_HEIGHT * scale_factor))
        self.rect = self.image.get_rect()
        
        self.rect.bottomleft = (50, SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT)  # Adjusted position

        #self.rect.bottomleft = (50, SCREEN_HEIGHT - GROUND_HEIGHT)
        self.speed = 5
        self.jump_power = -15
        self.gravity = 1
        self.vel_y = 0
        self.health = 100
        self.lives = 3
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.vel_y = self.jump_power
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        if self.rect.top >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.top = SCREEN_HEIGHT - GROUND_HEIGHT

       
     
# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.target_pos = target_pos
        self.speed = 10



    def update(self):
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        dist = max(1, abs(dx) + abs(dy))
        dx = dx / dist * self.speed
        dy = dy / dist * self.speed
        self.rect.centerx += dx
        self.rect.centery += dy
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0 or self.rect.bottom > SCREEN_HEIGHT or self.rect.top < 0:
            self.kill()
            
class Button:
    def __init__(self, text, position, size, color=(200, 200, 200), hover_color=(255, 255, 255), font_size=24):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(position, size)

    def draw(self, screen, hover=False):
        color = self.hover_color if hover else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        #self.image.fill(BLUE)
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - GROUND_HEIGHT - ENEMY_HEIGHT)  # Adjusted position

        #self.rect.bottomright = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - GROUND_HEIGHT)
        self.speed = 2
        self.health = 100

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.bottomright = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - GROUND_HEIGHT)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fire pro")

# Create sprite groups
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Main game loop
running = True
game_over = False
clock = pygame.time.Clock()
spawn_enemy_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_enemy_event, 3000)

background_image = pygame.image.load("background.jpeg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))




while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                # Shoot projectile
                if len(enemies) > 0:
                    target_enemy = random.choice(enemies.sprites())  # Choose a random enemy as the target
                    projectile = Projectile(player.rect.midright, target_enemy.rect.center)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)
    

        elif event.type == spawn_enemy_event and not game_over:
            # Spawn enemy randomly
            if random.random() < 2:  # Adjust probability as needed
                enemy = Enemy()
                enemy.rect.bottomright = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - GROUND_HEIGHT)
                all_sprites.add(enemy)
                enemies.add(enemy) 
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse events
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.is_clicked(mouse_pos) and game_over:
                  # Restart the game
                player.health = 100
                player.lives = 3
                player.score = 0
                game_over = False
                all_sprites.empty()
                projectiles.empty()
                enemies.empty()
                collectibles.empty()
                player.rect.bottomleft = (50, SCREEN_HEIGHT - GROUND_HEIGHT)
                all_sprites.add(player)


    if not game_over:
        all_sprites.update()

        
        # Check collisions
        enemy_hit = pygame.sprite.groupcollide(enemies, projectiles, True, True)
        if enemy_hit:
           player.score += 20

        enemy_hit_player = pygame.sprite.spritecollide(player, enemies, False)
        if enemy_hit_player:
           player.health -= 10
           if player.health <= 0:
               player.lives -= 1
               if player.lives <= 0:
                   game_over = True
                    
               else:
                   player.health = 100

        
        collectible_hit = pygame.sprite.spritecollide(player, collectibles, True)
        for collectible in collectible_hit:
            player.health += 20
            if player.health > 100:
                player.health = 100
            player.score += 10

        # Add enemies and collectibles
        if len(enemies) < 2:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

       

        # Drawing
        screen.fill((0, 0, 0))
        screen.blit(background_image,(0,0))
        all_sprites.draw(screen)

        # Health bar
        pygame.draw.rect(screen, GREEN, (20, 20, player.health * 2, 10))
        pygame.draw.rect(screen, WHITE, (20, 20, 200, 10), 2)

        # Lives
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))

        # Score
        score_text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(score_text, (20, 50))

        # Game over screen
        if game_over:
            restart_button = Button('Restart', (300, 400), (200, 50))
            restart_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.is_clicked(mouse_pos):
                        # Restart the game
                        player.health = 100
                        player.lives = 3
                        player.score = 0
                        game_over = False
                        all_sprites.empty()
                        projectiles.empty()
                        enemies.empty()
                        collectibles.empty()
                        player.rect.bottomleft = (50, SCREEN_HEIGHT - GROUND_HEIGHT)
                        all_sprites.add(player)
   
          
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
