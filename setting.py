
class settings:
    """A class settings for alien invasion"""

    def __init__(self):
        """Initialize the game's static settings"""
        # screen setting
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (101,178,216)
        # ship settings
        # self.ship_speed = 1.5
        self.ship_limit=3
        #alien settings
        # self.alien_speed=1.0
        self.fleet_drop_speed=10
        #fleet_direction represents right ;-1 represent left
        # self.fleet_direction=1
        
        #bullet settings
        # self.bullet_speed=1.5
        self.bullet_width=5
        self.bullet_height=15
        self.bullet_color=(178,246,23)
        self.bullets_allowed=3
        
        #How quickly the game speeds up
        self.speedup_scale=1.1
        #How quickly alien point values incresing
        self.score_scale=1.5
        self.initialize_dynamic_settings()
        
        #alien ships setting
        # self.screen_hight=1200
        # self.screen_width=900
        # self.ship_color=(150,123,45)
    def initialize_dynamic_settings(self):
        """initialize the setting that changes through out the game"""
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.alien_speed=1.0
        
        # Scoring
        self.alien_points=50
        
        # fleet_direction of 1 represents right; -1 represent
        self.fleet_direction=1 
    def increase_speed(self):
        """Increase speed settings and aliens points values"""
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        
        self.alien_points=int(self.alien_points*self.score_scale)
        print(self.alien_points)
        