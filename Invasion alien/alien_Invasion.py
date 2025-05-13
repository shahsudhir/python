import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Set up full-screen display
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        #create an instance to store game statstics
        self.stats=GameStats(self)

        self.ship = Ship(self)  # Corrected class name
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Load bullet sound
        self.bullet_sound = pygame.mixer.Sound('bullet.wav')  # <-- you need bullet.wav file in your project folder

        self._create_fleet()
        #make the play button
        self.play_button=Button(self, "play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.clock.tick(60)
            self._update_screen( )


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type== pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullet_sound.play()  # <-- play sound when bullet fired!

    def _update_bullets(self):
        """Update bullet positions and remove off-screen bullets."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        #get rid of bullets that have dissappered 
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

      

    

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update the positions of all aliens."""
        self._check_fleet_edges()
        self.aliens.update()

          #Look foe alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

            #look for aliens hitting the bottom of the screen 
            self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _ship_hit(self):
        #respond to the ship beign to hit by an alien
       if self.stats.ships_left>0:



        #Decrement ships_left
        self.stats.ships_left-=1

        #get rid of any remainning aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        #create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        #pause
        sleep(0.5)
       else:
           self.stats.game_active=False
           pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        #check if any aliens reached the bottom of the screen
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        #start a new game when the player click play
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset the game settings
            self.settings.initialize_dynamic_settings()

        
            #reset the game statistics
            self.stats.game_active=True

            #get rid of any remaining aliens bullets
            self.aliens.empty()
            self.bullets.empty()
            #create a new fleet and center the ship 
            self._create_fleet()
            self.ship.center_ship()
            #hide the mouse cursor
            pygame.mouse.set_visible(False)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
