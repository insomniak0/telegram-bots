from enums import Game_Settings
class Settings:
    def __init__(self):
        # enum default settings
        self.def_letters = Game_Settings.LETTERS.value[0]
        self.tries = Game_Settings.TRIES.value[0]
        self.current_try=0

    #getters
    def get_amount_letters(self):
        return int(self.def_letters)

    def get_tries(self):
        return self.tries

    #setters
    def set_amount_letters(self,_def_letters):
        self.def_letters = _def_letters

    def set_tries(self,_tries):
        self.tries = int(_tries)

    def set_current_try(self,n=1):
        self.current_try+=n

    def get_current_try(self):
        return self.current_try

    def clear_data(self):
        #for new game.
        self.current_try = 0

    def check_lose(self):
       #check if user lost
       #print(self.current_try)
        #print(self.tries)
        if self.current_try >= self.tries:
            return True
        return False

