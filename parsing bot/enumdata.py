from enum import Enum

class General(Enum):
    OFFSET=60 #it's limitation of parsing site.
    FILE_WAY="output/" # all files will be saved here.

class Categories(Enum):
    #site has more categories. These are only for example.

    CATEGORIES=[{'name':'knives','cat_id':2},
                {'name': 'gloves', 'cat_id': 13},
                {'name': 'sniper riffles', 'cat_id': 4},
                {'name': 'gun', 'cat_id': 5},
                {'name': 'SMG', 'cat_id': 6},
                ]
    #bot settings
    SETTINGS=[{'name':'min price'},
              {'name':'max price'},
              {'name':'discount'}]


#TODO: Save modes: json or xls.

#modes or states of bot.
class Modes(Enum):
    START='start'
    SETTINGS='settings'
    SET_MIN_PRICE='set min price:'
    SET_MAX_PRICE='set max price:'
    SET_DISCOUNT='set discount:'
    PARSING='parsing'

#this code could be changed for localization purposes.
class Texts(Enum):
    START_TEXT="Hello, I'm Bot, who can parse discounts from cs.money and save them to excel or json"
    COMMANDS_APPENDIX="hit /settings to change discount % "
    SETTINGS_CHANGED="Ok. Here is the settings now: min price is {}, max price is {}, discount {}%"
    CHOOSE_CATEGORY="Choose on of categories:"
    WHAT_MIN_PRICE = "What min. price would you like to defind?"
    WHAT_MAX_PRICE = "What max. price would you like to defind?"
    WHAT_DISCOUNT = "What discount would you like to defind?"
    CATEGORY_SELECTED = "You select category {}. To start parsing, please use /collectdata command."
    DATA_IS_READY = "Data is collected"
    PROCESSING = "Data is collecting..."