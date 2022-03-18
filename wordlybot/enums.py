from enum import Enum

class Colors(Enum):
    GREY='🟣'
    GOLD='🟡'
    GREEN='🟢'


class Game_Settings(Enum):
    '''game settings. Information is using in inline buttons too'''
    LETTERS = [5,6,7,8,9,10]
    TRIES = [5,7,9]