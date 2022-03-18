"""
Wordle bot
Author: Evgeni Lapanik
"""
from settings import Settings
from wordly import Wordly
from bot import Bot
def main():

    set = Settings()
    w = Wordly(set)
    word = w.start_round()
    print(w.get_pole())


    wbot = Bot()
    wbot.set_word(w.get_pole())# draw string with purple circle.
    wbot.set_correct_word(word)# add hidden word to bot
    wbot.set_settings(set) #link settings object
    wbot.set_wordly(w) #link bot with wordly object



    wbot.start_polling()


if __name__ == '__main__':
    main()
