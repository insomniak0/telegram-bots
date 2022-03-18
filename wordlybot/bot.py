import telebot
from telebot import types
import os
from enums import Game_Settings

class Bot:
    def __init__(self):
        print("init bot")
        self.API = os.environ.get("TELEGRAM_API") #enviroment variable for api
        self.wbot = telebot.TeleBot(self.API)
        self.chat_id = 0
        self.settings = None # variable for link on settings object.
        self.wordly = None # variable for link on wordle object
        self.display_word = "" # string for bot.send
        self.settings_mode = 'amount' # variable for settings.

        # apendix is used in several place in the code. I separeted it,
        # to comply with principals DRY - don't repeat yourself
        self.appendix="Please send /play command to start the game\n\n" \
                      "/len - change amount letters in the word\n"\
                      "/attempts - change amount of attemp per word"

        self.photo=[] # photo - just list of strings with all attempts that user made.

        # The one way to use bot api in the separate class is to use docarator methods
        # inside __init__()
        @self.wbot.message_handler(commands=["tries"])
        def _process_command_start(message):
            self.process_command_start(message)
            self.chat_id = message.chat.id

        @self.wbot.callback_query_handler(func=lambda call: True)
        def _callback(call):
            self.callback(call)


        @self.wbot.message_handler(commands=["start"])
        def _process_command_start(message):
            self.process_command_start(message)
            self.chat_id = message.chat.id

        @self.wbot.message_handler(commands=["play"])
        def _process_play(message):
            self.play(message)


        # settings command, length of word
        @self.wbot.message_handler(commands=['len'])
        def _settings_word_length(message):
           self.settings_word_length(message)

        # settings command, amount of tries.
        @self.wbot.message_handler(commands=['attempts'])
        def _settings_attempts(message):
            self.settings_attempts(message)

        # handle of text that user has input
        @self.wbot.message_handler(content_types=['text'])
        def send_text(message):
            self.next_round(message)

    def make_keyboard(self,_values):
        '''method create Inline keyboard'''
        markup = types.InlineKeyboardMarkup()
        for value in _values:
            current_button = types.InlineKeyboardButton(text=f"{value}", callback_data=value)

            markup.add(current_button)
        return markup

    def settings_attempts(self,message):
        '''create keyboard with amount of attempts button '''
        self.settings_mode = 'attempts'
        markup = self.make_keyboard(Game_Settings.TRIES.value)
        self.wbot.send_message(message.chat.id, "Please, choose amount of tries:",
                               reply_markup=markup)


    def settings_word_length(self,message):
        '''settings. change word length'''
        self.settings_mode = 'length'
        markup = self.make_keyboard(Game_Settings.LETTERS.value)
        self.wbot.send_message(message.chat.id, "Please, choose length of the word:",
                               reply_markup=markup)


    def callback(self,call):
        '''handle press buttons events'''
        #function depends on mode variable.
        if self.settings_mode=='length':
            self.settings.set_amount_letters(call.data)
            self.wbot.send_message(call.message.chat.id, f"the current length of the word is {self.settings.get_amount_letters()}")
        if self.settings_mode=='attempts':
            self.settings.set_tries(call.data)
            self.wbot.send_message(call.message.chat.id, f"you have {self.settings.get_tries()} tries now")



    def next_round(self,message):
        '''compare word of user with hidden word and '''
        check_error = self.check_errors(message.text)

        if check_error==-1: #if there are no errors
            if not self.settings.check_lose(): # if last round wasn't final
                if not self.wordly.check_win(message.text): # if user still haven't won
                    compare_result =  self.wordly.compare(message.text) # compare two words
                    self.settings.set_current_try() # update attempt. It's +1 by default
                    round = self.settings.get_current_try() #getting current no of current try
                    self.wbot.send_message(message.chat.id,f"{round}. {compare_result}")
                    self.photo.append(compare_result) # for result photo save current string in photo list
                else:# if user won
                    self.final_message(message.chat.id,f"You won! \n the word is {self.wordly.get_answer()}")

            else:# if the last round was final
                self.final_message( message.chat.id, f"the word is {self.wordly.get_answer()}")


        else:#if there are some errors
            self.wbot.send_message(message.chat.id, check_error)

    def final_message(self,chat_id, _message):
        '''messages after end of the game'''
        self.wbot.send_message(chat_id,_message)
        self.make_photo(chat_id)
        self.wbot.send_message(chat_id, self.appendix)

    def make_photo(self,chat_id):
        '''show message with all attemps like in wordle'''
        self.wbot.send_message(chat_id,"\n".join(self.photo))
        self.photo.clear()


    def check_errors(self,_string):
        '''check inputted string'''
        #TODO: it's necessary to check and format inputted string

        print(self.settings)
        #if length of string is equal to letngth of hidden word.
        if len(_string) == self.settings.get_amount_letters():
            return -1

        #if inputted string has more chars than hidden word
        if len(_string)> self.settings.get_amount_letters():
            result = "your word is longer than hidden word"
        else: #if inputted string has less chars than hidden word
            result = "your word is shorer than hidden word"

        return result

    def play(self,message):
        '''starting game'''
        #print("word: " + self.display_word)
        round = self.wordly.start_round()
        self.wbot.send_message(message.chat.id,"" +round)

    def set_word(self,_word):

        #print("set new word")
        self.display_word = _word

    def set_settings(self,_settings):
        '''links bot with settings object'''
        #print("set settings into bot")
        self.settings=_settings
        print(self.settings)

    def process_command_start(self,message):
        '''starting message'''
        self.wbot.send_message(message.chat.id,"Hello I'm a little wordley bot. \n"+self.appendix)

    def start_polling(self):
        '''polling of the bot'''
        self.wbot.polling(none_stop=True)

    def set_correct_word(self,_word):

        self.correct_word = _word

    def set_wordly(self, _wordly):
        '''links bot with wordly object'''
        self.wordly =_wordly


