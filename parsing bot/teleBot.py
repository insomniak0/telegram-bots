import os
from aiogram import Bot, Dispatcher, executor, types
from enumdata import *
from request_handle import Request
from settings import Settings
from enumhandle import EnumHandle


class TeleBot:
    def __init__(self):
        self.dp: Dispatcher = None
        self.bot: Bot = None
        self.request: Request = None
        self.bot_settings: Settings = None
        self.enum_handler: EnumHandle = None
        self.result = []

    def set_enum_handler(self, _enumhandler):
        self.enum_handler = _enumhandler

    def activate_bot(self):
        print("status: activating bot")
        self.bot = Bot(token=os.environ.get("TELEGRAM_API"), parse_mode=types.ParseMode.HTML)
        print(self.bot)

    def set_despatcher(self, bot: Bot):
        self.dp = Dispatcher(bot)

    def init_settings(self, _settings: Settings):
        self.bot_settings = _settings

    def get_bot(self):
        print("returning bot:")
        print(self.bot)
        return self.bot

    def start_pulling(self):
        executor.start_polling(self.dp)

    def register_handlers(self):
        '''create handlers for all necessary commands and inputted text'''

        #It's better way than use decorators in __init__(), I belive.
        self.dp.register_message_handler(self.start, commands=['start'])

        self.dp.register_message_handler(self.settings, commands=['settings'])
        self.dp.register_message_handler(self.collect_data, commands=['collectdata'])
        self.dp.register_message_handler(self.menu_handler)

    async def start(self, messages: types.Message):
        '''handle start command'''

        #definately this method is too heave to read. Should be separated on several lesser methods.

        cur_mode =self.bot_settings.get_current_mode() # get current state of bot.

        #check if info is collected from site right now. if not - continure execute instruction
        if cur_mode == Modes.PARSING:
            return 0
        # Texts imported from enumdata
        self.bot_settings.set_current_mode(Modes.START.value)

        #simple check not to show start message in future iterations.
        if self.bot_settings.get_is_started()== 0:
            self.bot_settings.set_is_started(1)
            await self.bot.send_message(chat_id=messages.chat.id, text=Texts.START_TEXT.value)

        await self.bot.send_message(chat_id=messages.chat.id, text=Texts.COMMANDS_APPENDIX.value)

        k = self.show_keyboard()
        await messages.answer(Texts.CHOOSE_CATEGORY.value, reply_markup=k)

    async def collect_data(self, message: types.Message):
        '''collecting data from site'''
        # if collecting data is still occured script should do nothing.
        if self.bot_settings.get_current_mode() == Modes.PARSING:
            return 0

        await self.bot.send_message(message.chat.id,text=Texts.PROCESSING.value)
        self.result = self.request.collect_data()
        self.request.dump_to_file(message.chat.id)

        #send file with data to the user.
        #TODO: add options, use json or xls.
        file = open(General.FILE_WAY.value+self.bot_settings.get_file_name(), 'rb')

        await self.bot.send_message(message.chat.id, text=Texts.DATA_IS_READY.value)
        await self.bot.send_document(chat_id=message.chat.id, document=file,)
        #await self.bot.send_message(chat_id=message.chat.id, text=Texts.COMMANDS_APPENDIX.value,reply_markup=self.show_keyboard())

        #not the best decision, I suppose.
        await self.start(message)

    def init_requests(self, r: Request):
        self.request = r

    async def settings(self, messages: types.Message):
        '''show settings'''
        if self.bot_settings.get_current_mode() == Modes.PARSING:
            return 0

        print("handle settings command")
        #show keyboard with settings.
        self.bot_settings.set_current_mode(Modes.SETTINGS.value)
        k = self.show_keyboard()
        await self.bot.send_message(messages.chat.id,
                                    text="Open settings..", reply_markup=k)

    async def menu_handler(self, message: types.Message):
        '''handle inputted data'''
        #if collecting data is still occured script should do nothing.
        if self.bot_settings.get_current_mode() == Modes.PARSING:
            return 0

        cur_mode = self.bot_settings.get_current_mode()
        chat_id = message.chat.id

        #mode that shows seelected category
        if cur_mode == Modes.START.value:
            cat_id = self.bot_settings.find_cat_id(message.text)
            print(cat_id)
            self.bot_settings.set_current_type(cat_id)
            print(self.bot_settings.get_current_type())

            await self.bot.send_message(message.chat.id, text=Texts.CATEGORY_SELECTED.value.format(message.text))

        #depends on mode show settings
        elif cur_mode == Modes.SETTINGS.value:
            # not the best decision.

            if message.text == Categories.SETTINGS.value[0]['name']:
                # min price
                self.bot_settings.set_current_mode(Modes.SET_MIN_PRICE)
                await self.bot.send_message(chat_id, text=Texts.WHAT_MIN_PRICE.value)

            elif message.text == Categories.SETTINGS.value[1]['name']:
                # max price
                self.bot_settings.set_current_mode(Modes.SET_MAX_PRICE)
                await self.bot.send_message(chat_id, text=Texts.WHAT_DISCOUNT.value)
            elif message.text == Categories.SETTINGS.value[2]['name']:
                # discount
                self.bot_settings.set_current_mode(Modes.SET_DISCOUNT)
                await self.bot.send_message(chat_id, text=Texts.WHAT_DISCOUNT.value)


        #depends on current mode change the data in settings
        elif cur_mode == Modes.SET_MIN_PRICE:
            await self.show_updated_info(self.bot_settings.set_min_price, chat_id, message)
        elif cur_mode == Modes.SET_MAX_PRICE:
            await self.show_updated_info(self.bot_settings.set_max_price, chat_id, message)
        elif cur_mode == Modes.SET_DISCOUNT:
            await self.show_updated_info(self.bot_settings.set_discount, chat_id, message)

    async def show_updated_info(self, _setting, chat_id, message):
        try:
            self.bot_settings.set_current_mode(Modes.SETTINGS.value)
            _setting(message.text)
            await self.bot.send_message(chat_id,
                                        self.enum_handler.update_settings_text(),
                                        reply_markup=self.show_keyboard())

        except Exception as e:
            print(e)

    def show_keyboard(self):
        '''create keyboards'''
        #TODO: move keyboard to separate class
        #TODO: add keyboard with format files (xls, json).
        print("create keyboard")

        l = []
        mode = self.bot_settings.get_current_mode()
        print(f"current mode: {mode}")
        #loop through categories in enum and add buttons.
        if mode == Modes.START.value:
            l = Categories.CATEGORIES.value
        elif mode == Modes.SETTINGS.value:
            #or loop through settings.
            l = Categories.SETTINGS.value
        print(l)
        start_buttons = [n['name'] for n in l]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*start_buttons)

        for n in Categories.CATEGORIES.value:
            print(n['name'])
        return keyboard

        # message handlers
