"""
Simple telegram bot for playing into quiz game.
Settings: it's possible to choose one of 3 question themes, and amount of questions.

API: https://opentdb.com/api_config.php

Author: Evgeni Lapanik
"""
import telebot
import os
import pprint
from settings import Settings
from helpers import Helpers


def main():
    set = Settings()
    helper = Helpers()
    #enivroment variable
    api_key_telegram = os.environ.get("TELEGRAM_API")
    bot = telebot.TeleBot(api_key_telegram)

    # handle events of press button.
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        '''function handle press  inline button events'''
        set.set_current_question()
        # now I'm sure, it was a strange way to send variables here. I could use one more varaible in settings class
        # but I decided send mode variable together with responses. Ok.
        # Variable looks like: answer_mode.
        response = call.data.split("_")[0]
        mode = call.data.split("_")[1]
        #change amount of questions
        if mode == 'amount':
            set.set_default_amount(int(response))
            return start(call.message)
        #change category of questions
        if mode == 'category':
            set.set_default_category(response)
            return start(call.message)

        #print("user answer is " + response)
        #print("correct answer is" + set.get_correct_answer())

        if response == set.get_correct_answer():
            set.set_score()
            bot.send_message(chat_id=call.message.chat.id, text=f"Correct! ")

        else:
            bot.send_message(chat_id=call.message.chat.id, text=f"Wrong answer!\n "
                                                                f"The correct answer is {set.get_correct_answer()}.\n\n ")

        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Your score is {set.get_score()}/{set.get_default_amount()}")
        helper.next_question(call.message, bot, set)

    @bot.message_handler(commands=['play', 'repeat'])
    def repeat(message):
        #repeat and new game are the same.

        set.clear_data()
        set.set_bulk_of_questions(helper.get_questions(set))
        # pprint.pprint(bulk_of_questions)
        helper.next_question(message, bot, set)

    @bot.message_handler(commands=['theme'])
    def settings_theme(message):

        markup = helper.make_keyboard(set.get_categories().keys(), 'category')
        bot.send_message(message.chat.id, "Please, choose theme from the list:",
                         reply_markup=markup)

    @bot.message_handler(commands=['amount'])
    def settings_amount(message):
        markup = helper.make_keyboard(set.get_amounts_variants(), 'amount')
        bot.send_message(message.chat.id, "Please, choose amount of questions for your quiz:",
                         reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "<b>Hey there, I'm a super Quizbot!</b>", parse_mode='HTML')
        bot.send_message(message.chat.id,
                         f"Current theme of quize is <u>{set.get_default_category().title()}</u>. And amount of questions are {set.get_default_amount()}",
                         parse_mode='HTML')
        bot.send_message(message.chat.id, "to begin to play use /play command\n"
                                          f"if you want to change theme use, /theme command\n"
                                          f"if you want to change amount of questions, use /amount command")

    bot.polling(non_stop=True)


if __name__ == '__main__':
    main()
