import asyncio
import platform
import pygame
import random
from pygame.sprite import Sprite, Group

# Game settings
FPS = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BG_COLOR = (0, 0, 0)
SHIP_SPEED = 5
BULLET_SPEED = 10
BULLET_WIDTH = 15
BULLET_HEIGHT = 3
BULLET_COLOR = (255, 0, 0)
ALIEN_SPEED = 2
ALIEN_SPAWN_INTERVAL = 1  # Seconds between alien spawns
MAX_LIVES = 3

class Ship(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 50
        self.rect.centery = SCREEN_HEIGHT / 2
        self.y = float(self.rect.y)
        self.lives = MAX_LIVES
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.y -= SHIP_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.y += SHIP_SPEED
        self.rect.y = int(self.y)

class Bullet(Sprite):
    def __init__(self, ship):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.left = ship.rect.right
        self.rect.centery = ship.rect.centery
        self.x = float(self.rect.x)
    
    def update(self):
        self.x += BULLET_SPEED
        self.rect.x = int(self.x)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Alien(Sprite):
    def __init__(self, y_position):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.right = SCREEN_WIDTH
        self.rect.centery = y_position
        self.x = float(self.rect.x)
    
    def update(self):
        self.x -= ALIEN_SPEED
        self.rect.x = int(self.x)
        if self.rect.right < 0:
            self.kill()

def setup():
    global screen, ship, bullets, aliens, last_alien_spawn, score, font
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sideways Shooter")
    ship = Ship()
    bullets = Group()
    aliens = Group()
    last_alien_spawn = pygame.time.get_ticks() / 1000
    score = 0
    font = pygame.font.Font(None, 36)

def update_loop():
    global last_alien_spawn, score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.add(Bullet(ship))
    
    ship.update()
    bullets.update()
    aliens.update()
    
    # Spawn new aliens
    current_time = pygame.time.get_ticks() / 1000
    if current_time - last_alien_spawn > ALIEN_SPAWN_INTERVAL:
        y_pos = random.randint(0, SCREEN_HEIGHT)
        aliens.add(Alien(y_pos))
        last_alien_spawn = current_time
    
    # Check for bullet-alien collisions
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    score += len(collisions)  # Increment score for each alien hit
    
    # Check for alien-ship collisions
    ship_hits = pygame.sprite.spritecollide(ship, aliens, True)
    for hit in ship_hits:
        ship.lives -= 1
        if ship.lives <= 0:
            return False  # End game when lives run out
    
    # Draw everything
    screen.fill(BG_COLOR)
    screen.blit(ship.image, ship.rect)
    bullets.draw(screen)
    aliens.draw(screen)
    
    # Draw lives and score
    lives_text = font.render(f"Lives: {ship.lives}", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 50))
    
    pygame.display.flip()
    return True

async def main():
    setup()
    while True:
        if not update_loop():
            break
        await asyncio.sleep(1.0 / FPS)
    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())