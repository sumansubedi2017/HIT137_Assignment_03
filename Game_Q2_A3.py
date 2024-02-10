#Import the pygame module for game development.
import pygame
import random
import sys
import os

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


LEVEL_1 = 1
LEVEL_2 = 2
LEVEL_3 = 3

current_level = LEVEL_1


# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Get the current working directory
current_directory = os.getcwd()
print("Current working directory:", current_directory)


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        scale_factor = 2  # Adjust as needed
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH * scale_factor, PLAYER_HEIGHT * scale_factor))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (50, SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT)  # Adjusted position
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
        self.timer = 180 # 60 frames = 1 second

    def update(self):
        # Calculate vertical distance
        dy = self.target_pos[1] - self.rect.centery
        dist = max(1, abs(dy))
        
        # Calculate vertical movement
        dy = dy / dist * self.speed
        self.rect.centery += dy

        # Check if the projectile reaches the target vertically
        if (dy > 0 and self.rect.centery >= self.target_pos[1]) or (dy < 0 and self.rect.centery <= self.target_pos[1]):
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
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = 2
        self.health = 100
        self.shoot_delay = 1000  # Delay between shots in milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()
                
            

       

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

backgrounds = [
    pygame.image.load("background.jpeg").convert(),
    pygame.image.load("background.jpeg").convert(),
    pygame.image.load("background.jpeg").convert()
]

current_level = LEVEL_1
background_image = backgrounds[current_level]
level_enemy_positions = [
    [(700, 400), (600, 300), (500, 200)],
    [(700, 100), (600, 200), (500, 300)],
    [(700, 300), (600, 250), (500, 200)]
]
game_paused = False
while running:
    
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                if len(enemies) > 0:
                    target_enemy = random.choice(enemies.sprites())
                    projectile = Projectile(player.rect.midright, target_enemy.rect.center)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)


        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_over:
                if restart_button.is_clicked(mouse_pos) and game_over:
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
            elif game_paused:
                game_paused = False

            else:
                pass 

    if not game_over:
        all_sprites.update()

        

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
        
        if len(enemies) < 2:
            enemy = Enemy(random.choice(level_enemy_positions[current_level]))
            all_sprites.add(enemy)
            enemies.add(enemy)
        

        if player.score >= 100 and current_level == LEVEL_1:
            if current_level< LEVEL_2:                      
                        current_level = LEVEL_2
                        player.score = 0
                        level_enemy_positions[1] = [(700, 400), (600, 300), (500, 200), (400, 100)]
                        level_text = font.render(f"Level: {current_level}", True, WHITE)

                        background_image = pygame.image.load("level2.jpg").convert()
                        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                        for enemy in enemies:
                            enemy.speed = 3


                        


        if  player.score >=300 and current_level == LEVEL_2:
                        current_level = LEVEL_3
                        player.score= 0
                        level_enemy_positions.append([(700, 300), (600, 250), (500, 200)])
                        background_image = pygame.image.load("level3.jpg").convert()
                        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                        # Increase enemy speed for level 3
                        for enemy in enemies:
                            enemy.speed = 5
                            
                   



        if player.score >= 500 and current_level ==LEVEL_3:
            game_paused =True
            font = pygame.font.Font(None, 48)
            congrats_text = font.render("CONGRATULATIONS! You completed Level 3!", True, GREEN)
            screen.blit(congrats_text, (200, 200))
            pygame.display.flip()

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        pygame.draw.rect(screen, GREEN, (20, 20, player.health * 2, 10))
        pygame.draw.rect(screen, WHITE, (20, 20, 200, 10), 2)

        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))

        score_text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(score_text, (20, 50))

        level_text = font.render(f"Level: {current_level}", True, WHITE)
        screen.blit(level_text, (20, 80))

        if game_over:
            restart_button = Button('Restart', (300, 400), (200, 50))
            restart_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.is_clicked(mouse_pos):
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
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    game_paused = False  # Unpause the game when any key is pressed
                    screen.fill((0, 0, 0))
                    screen.blit(background_image, (0, 0))
                    all_sprites.draw(screen)

                    pygame.draw.rect(screen, GREEN, (20, 20, player.health * 2, 10))
                    pygame.draw.rect(screen, WHITE, (20, 20, 200, 10), 2)

                    font = pygame.font.Font(None, 36)
                    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
                    screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))

                    score_text = font.render(f"Score: {player.score}", True, WHITE)
                    screen.blit(score_text, (20, 50))

                    level_text = font.render(f"Level: {current_level}", True, WHITE)
                    screen.blit(level_text, (20, 80))

                    pygame.display.flip()

    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
