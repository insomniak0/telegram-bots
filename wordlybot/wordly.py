"""
Basic wordly methods.

"""
# random words module needs also pip install pyyaml
import random_word as rw
from enums import Colors

class Wordly:
    def __init__(self,_settings):
        self.random_word = rw.RandomWords()
        self.settngs = _settings
        self.word=""
        pass


    def get_new_word(self):
        '''method return new word of length that defined in setting's get_def_letters()'''
        # get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10,
        #                  minDictionaryCount=1, maxDictionaryCount=10, minLength=5, maxLength=10)
        #print("settings:"+ str(self.random_word.get_random_word()))

        self.word =str(self.random_word.get_random_word(hasDictionaryDef="true",
                                                        includePartOfSpeech="noun",
                                                        minDictionaryCount=1,
                                                        maxDictionaryCount=10,
                                                        minLength=self.settngs.get_amount_letters(),
                                                        maxLength=self.settngs.get_amount_letters()))

        print("secret word is "+self.word)
        return self.word.lower()

    def get_pole(self):
        print("==create new string of elements==")
        string = "".join(["*" for n in self.word])

        return string

    def start_round(self):
        self.settngs.clear_data()
        self.word  = self.get_new_word()
        round = self.settngs.get_current_try()
        return f"{round}. "+" ".join([Colors.GREY.value for n in self.word])

    def get_answer(self):
        return self.word

    def check_win(self, _guess):
        if _guess == self.word:
            return True
        return False

    def compare(self,_guess):
        '''compare two words and return a string with circle of different colors.'''
        #print("user guess: "+_guess)
        #print("secret word: "+self.word)
        g = [n for n in _guess] # rebuild string into list. Long way better is here https://www.geeksforgeeks.org/python-program-convert-string-list/
        return_string = []
        #print(str(self.word.find("a")))
        for n in g:
            if _guess.find(n)==self.word.find(n): #if position and letter of guess and hidden word are equal
                return_string.append(Colors.GREEN.value)
            elif self.word.find(n)>-1: #if there is a letter in the hidden word
                return_string.append(Colors.GOLD.value)
            else: #in other case the letter wasn't finded.
                return_string.append(Colors.GREY.value)


        return " ".join(return_string) # a little bit format.