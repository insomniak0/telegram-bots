# Author: Evgeni Lapanik
# Description: The bot, which parse information about discounts of cs marketplace to json file.

from request_handle import Request
from settings import Settings
from teleBot import TeleBot
from enumhandle import EnumHandle
import asyncio


def main():
    bt = TeleBot()
    bt.activate_bot()
    bt.set_despatcher(bt.get_bot())
    bt.register_handlers()

    s = Settings()  # settings object. All necessary changable information are stored here.
    r = Request()  # working with url requests and creating json files.

    r.init_settings(s)
    bt.init_settings(s)

    eh = EnumHandle()  # object helps find some information in enumdata.py
    eh.set_settings(s)

    bt.init_requests(r)
    bt.set_enum_handler(eh)
    bt.start_pulling()


print(__name__)

if __name__ == "__main__":
    asyncio.run(main())
