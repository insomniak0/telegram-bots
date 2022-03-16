"""
Settings of the quizbot
"""

class Settings():

    def __init__(self):

        self.current_question = 0 #rounds of game
        self.correct_answer = ""
        self.score = 0
        self.default_category = 'history'
        self.default_amount = 10
        self.amount_variants = [5, 10, 15, 20]
        # open trivia db has much more themes. I choose only several for example.
        self.categories = {
            'history': 23,
            'video games': 15,
            'general knowledge': 9,
        }
        self.bulk_of_questions = {}# all questions will be saved here

    #getters
    def get_current_question(self):
        return self.current_question
    def get_correct_answer(self):
        return self.correct_answer
    def get_score(self):
        return self.score
    def get_default_category(self):
        return self.default_category
    def get_default_amount(self):
        return self.default_amount
    def get_amounts_variants(self):
        return self.amount_variants
    def get_categories(self):
        return self.categories
    def get_bulk_of_questions(self):
        return self.bulk_of_questions

    #setters
    def set_current_question(self,q=1):
        '''variable for counting of rounds. Defaultly it adds 1 to the count'''
        self.current_question+=q

    def set_correct_answer(self,s):
        self.correct_answer = s

    def set_score(self,s=1):
        self.score+=s

    def set_default_category(self,s='history'):
        self.default_category=s

    def  set_default_amount(self,a=10):
        '''amount of questions for trivia. default amount is 10. can be change in settings mode'''
        self.default_amount=a

    def  set_bulk_of_questions(self,b):
        self.bulk_of_questions=b


    def clear_data(self):
        '''clear all data for the new game'''
        self.score=0
        self.current_question = 0

