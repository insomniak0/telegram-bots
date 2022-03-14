# simple bot for telegram to check weather
import telebot
from telebot import types
import os
import requests
import re
import emoji

# the way to use enviroment keys in windows https://www.youtube.com/watch?v=IolxqkL7cD8
# how to open advanced system settings by cmd http://www.tenuser.com/spec/properties.htm
api_key_telegram = os.environ.get('TELEGRAM_API')
api_key_weather = os.environ.get('WEATHER_API')

# Dict with emojis. Unfortunately there are not so many emojis for weather.
emojis_dict = {
    1: ":sun:",
    2: ":sun:",
    3: ":cloud:",
    4: ":cloud:",
    9: ":umbrella:",
    10: ":umbrella:",
    11: ":zap:",
    13: ":snowflake:",
    50: ":foggy:",
}
# This variable are used to define
current_mode = 1

# four main modes for prediction. first mode - for current weather
predict_modes = {
    1: 'Jetzt',
    12: '12+ Stunden',
    24: '24+ Stunden',
    36: '36+ Stunden',
    48: '48+ Stunden',
}


# function make a menu for /periods command with prediction buttons.
def make_keyboard(type=0):
    markup = types.InlineKeyboardMarkup()
    #TODO: row doesn't work. Probably because you need to add to markap all buttons in one time.
    markup.row_width = 2
    for key, value in predict_modes.items():
        if key != type:
            # print("but "+value,key)
            # callbck_data shouldn't be 0 or there will be 400 arised
            but = types.InlineKeyboardButton(text=value, callback_data=key)
            markup.add(but)
            # print(but)

    # print("=============")
    return markup

#request url for a open weather api.
def make_url(city, mode):
    if mode == 1:
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + api_key_weather
        url = url.format(city)
    else:
        #difference there is additional parameter cnt - it responsible for prediction of weather in future hours
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&cnt={}&units=metric&appid=" + api_key_weather
        url = url.format(city, mode)
    return url

#main bot funciton
def botfunc():
    bot = telebot.TeleBot(api_key_telegram)
    #current_mod variable should be global otherwise it's not working.
    global current_mode

    #command for choosing of prediction period
    @bot.message_handler(commands=['period'])
    def settings(message):
        markup = make_keyboard(current_mode)
        bot.send_message(message.from_user.id, "Wählen Sie bitte Vorhersageperiod:",
                         reply_markup=markup)

    #initial messages for user by starting chat
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.from_user.id,
                         "Die Wetter wird für nächste Period gezeigt:" + predict_modes.get(current_mode))
        bot.send_message(message.from_user.id, "Um Period zu ändern,schreiben Sie bitte /period Befehl")
        bot.send_message(message.from_user.id, "An welche Stadt haben Sie interesse?")

    #handle events of press button.
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        global current_mode
        print(call)
        # without int() this variable doesn't work correctly
        current_mode = int(call.data)
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Ok. Ich werde Wetter für {predict_modes.get(current_mode)} vorhersagen")

    @bot.message_handler(func=lambda message: True)
    def handle_text(message):
        global current_mode
        print("current mode:" + str(current_mode))
        city = message.text
        url = make_url(city, current_mode)
        chat_message = "Ok. Ich suche Information  über {}. Period: {}"
        bot.send_message(message.chat.id, chat_message.format(city.title(), predict_modes.get(current_mode)))

        #trying to find information about city.
        try:
            # by format you are insert city to the {} in url.
            res = requests.get(url).json()

            #json of weather api.
            temp = res['main']['temp']
            icon = res['weather'][0]['icon']

            result = 'In {} ist {}° '.format(city.title(), temp)

            # To get emoji, 1st of all we need to get number of icon from the string
            icon_number = int(re.search(r'\d+', icon).group())
            # and get value from dictionary where the number above is a key
            icon_emoji = emojis_dict.get(icon_number)

            # int(re.search(r'\d+', string1).group())

            result += emoji.emojize(icon_emoji)

        #exception if city haven't been found.
        except Exception as e:
            # to find the name of exception use this: e.__class__.__name__
            result = "Sorry, keine {} finden kann".format(city)
            print(e.__class__.__name__)
        bot.send_message(message.chat.id, result)

    #bot functions should be above this string.
    bot.polling(none_stop=True)


def main():
    print(api_key_telegram)
    print(api_key_weather)
    botfunc()


if __name__ == '__main__':
    main()
