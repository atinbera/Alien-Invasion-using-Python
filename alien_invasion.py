import sys
from time import sleep
import pygame
from setting import settings
from game_stats import Gamestats
from scoreboard import Scoreboard   
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """This class manage game assest and behavior"""

    def __init__(self):#constructor
        """Initialize the game and create resources"""
        pygame.init()
        self.settings = settings()

        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        #Create an instance to store game statistics
        # and create a Scoreboard
        self.stats=Gamestats(self)
        self.sb=Scoreboard(self)
        self.ship = Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        
        #make the play button
        self.play_button=Button(self,"play")
        # set the background color
        # self.bg_color=(230,230,230)

    def run_game(self):
        """Start the main game using for loop."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                # self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            # get rid of bullets that have disappered.
    def _update_bullets(self):
        """update positions of bullets and get rid of the old bullets"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """Respond the bullet alien collisions"""
        #Remove  any aliens which is collided by bullets
        #check for any bullets that have hit aliens
        # if so get rid of the bullets and the aliens
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            #destroy exiting bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()  
            self.settings.increase_speed()  
        #increase level
        self.stats.level+=1
        self.sb.prep_level()
        # print(len(self.bullets))
        

    def _update_screen(self):
        """Update imageon the screen and flip the image"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        """Make the most recently screen visible"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        #draw the score information
        self.sb.show_score()
        
        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
        
        

    def _check_events(self):
        """Watch for the mouse and keyboard"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key==pygame.K_q or event.key==pygame.K_ESCAPE:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
        

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
        
    def _create_fleet(self):
        """Create the fleet of aliens"""
        # make an alien
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width-(2* alien_width)
        number_aliens_x=available_space_x//(2*alien_width)
        #determine the number of rows of aliens that fit onn the screen
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height -
                           (3*alien_height)-(ship_height))
        number_rows=available_space_y // (2*alien_height)
        #create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)
            
            #create an alien and place it in the row
            
            
    def _create_alien(self,alien_number,row_number):
        """Create an alien and place it in the row"""
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width + 2* alien_width* alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height *row_number
        self.aliens.add(alien)

            # """Redraw the screen during each pass through the loop"""

    def _update_aliens(self):
        """Update the position of the alien's in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        
        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            print("Ship hit!!!")
            
        #look for aliens hiting bottom of the screen
        self._check_aliens_bottom()
        
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left>0:
            #Decrement ships_left and update scoreboard
            self.stats.ships_left-=1
            self.sb.prep_ships()
        
            #get ridof any aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            
            #Create a new fleet and centre the ship
            self._create_fleet()
            self.ship.center_ship()
            #pause
            sleep(0.5)
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)
            
    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen or not"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break
        
    def _check_play_button(self,mouse_pos):
        """Starts a new game when players clicks play"""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
        # if self.play_button.rect.collidepoint(mouse_pos):
            #Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            
            #Create a new flip and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            #Hide the cursor
            pygame.mouse.set_visible(False)
        
if __name__ == "__main__":

    """Make a game and run the instance"""
    ai = AlienInvasion()
    ai.run_game()
