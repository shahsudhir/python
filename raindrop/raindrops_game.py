import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Raindrops")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

# Raindrop settings
GRID_ROWS = 5
GRID_COLS = 5
RAINDROP_SIZE = 20
GRID_SPACING = 100
FALL_SPEED = 5

# Calculate grid offsets to center it
GRID_WIDTH = GRID_COLS * GRID_SPACING
GRID_HEIGHT = GRID_ROWS * GRID_SPACING
OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH) // 2 + GRID_SPACING // 2
OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT) // 2 + GRID_SPACING // 2

# Raindrop class
class Raindrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), RAINDROP_SIZE // 2)
            points = [
                (self.x, self.y - RAINDROP_SIZE // 2),
                (self.x - RAINDROP_SIZE // 4, self.y + RAINDROP_SIZE // 2),
                (self.x + RAINDROP_SIZE // 4, self.y + RAINDROP_SIZE // 2)
            ]
            pygame.draw.polygon(surface, BLUE, points)

    def update(self):
        if self.active:
            self.y += FALL_SPEED
            if self.y > SCREEN_HEIGHT + RAINDROP_SIZE:
                self.active = False

# Create grid of raindrops, organized by rows
def create_row(y_offset):
    """Create a single row of raindrops at a given y position."""
    row = []
    for col in range(GRID_COLS):
        x = OFFSET_X + col * GRID_SPACING
        row.append(Raindrop(x, y_offset))
    return row

raindrops = []
for row in range(GRID_ROWS):
    y = OFFSET_Y + row * GRID_SPACING
    raindrops.append(create_row(y))

# Game loop variables
FPS = 60
clock = pygame.time.Clock()
running = True

def setup():
    pass

async def update_loop():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update raindrops
        for row in raindrops:
            for raindrop in row:
                raindrop.update()

        # Check if any row is completely inactive
        rows_to_remove = []
        for row in raindrops:
            if all(not raindrop.active for raindrop in row):
                rows_to_remove.append(row)

        # Remove dead rows and add new rows at the top
        for dead_row in rows_to_remove:
            raindrops.remove(dead_row)
            # Insert a new row at the top with y slightly above the screen
            new_row_y = -GRID_SPACING
            raindrops.insert(0, create_row(new_row_y))

        # Draw everything
        screen.fill(BLACK)
        for row in raindrops:
            for raindrop in row:
                raindrop.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

async def main():
    setup()
    await update_loop()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
