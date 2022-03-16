"""
Helpers for the quizbot
"""
import requests
import random
from telebot import types
import html

class Helpers:
    def __init__(self):
        pass

    def get_questions(self,set):
        '''method retrieves information from open trivia database'''
        string = "https://opentdb.com/api.php?amount={}&category={}".format(set.get_default_amount(),
                                                                            set.get_categories()[set.get_default_category()])
        print(string)
        return requests.get(string).json()


    def mix_answers(self,answers=[], correct_answer=""):
        '''open trivia database separates wrong and correct answers, this method mix them for buttons'''
        answers.append(correct_answer)
        # shuffle list of strings. With string random.shuffle doesn't work
        answers = random.sample(answers, len(answers))
        return answers

    def make_keyboard(self,buttons,mode='answer'):
        '''creating inline buttons for game and choosing theme of trivia and amount of questions'''
        markup = types.InlineKeyboardMarkup()

        for button in buttons:
            callback = str(button)+"_"+mode
            print(callback)
            current_button = types.InlineKeyboardButton(text=button, callback_data=callback)

            markup.add(current_button)
            # print(but)

        return markup

    def next_question(self,message,bot,set):
        global current_question, correct_answer,default_amount
        bulk_of_questions = set.get_bulk_of_questions()
        #if number of question is above limit:
        if set.get_current_question() >= set.get_default_amount()-1:
            #than end game.
            bot.send_message(message.chat.id, f"<b>Your score: {set.get_score()}/{set.get_default_amount()} </b>\n"
                                              f"To play again use command /repeat\n"
                                              f"if you want to change theme use, /theme command\n"
                                              f"if you want to change amount of questions, use /amount command",parse_mode='HTML')
        else:
            # sometimes in responses in trivia there are special symbols like &nbsp; html.unescape convert them to the corresponding Unicode characters.
            question = html.unescape(bulk_of_questions['results'][set.get_current_question()]['question'])
            #set.get_current_question() -current question
            answers = bulk_of_questions['results'][set.get_current_question()]['incorrect_answers']
            answers = [html.unescape(answer) for answer in answers]
            set.set_correct_answer(html.unescape(bulk_of_questions['results'][set.get_current_question()]['correct_answer']))

            #mix correct and incorrect answers together. Trivia db separate them.
            answers_markup = self.make_keyboard(self.mix_answers(answers, set.get_correct_answer()))

            # pprint.pprint(bulk_of_questions)
            bot.send_message(message.chat.id, f"Question No.{set.get_current_question() + 1} \n{question}",
                             reply_markup=answers_markup)