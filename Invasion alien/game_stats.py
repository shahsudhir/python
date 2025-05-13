class GameStats:
    #track statistics for alien Invansion

    def __init__(self, ai_game):
        #initialize statistics
        self.settings=ai_game.settings
        self.reset_stats()

        #start Alien Invasion in an active state
        self.game_active=False


    def reset_stats(self):
        #initializing statistics that can change during the game 
        self.ships_left= self.settings.ship_limit
        self.score=0
         