import requests
from datetime import datetime
from settings import Settings
from user_agent import generate_user_agent, generate_navigator
from enumdata import General
import asyncio
import json
from enumdata import Modes


class Request:
    def __init__(self):
        self.settings = None #variable for settings object.
        self.result = [] #result is a dictionary to save in future json file
        pass

    def init_settings(self, _settings: Settings):
        '''init settings for Request object'''
        self.settings = _settings

    def get_url(self, _offset: int):
        '''create URL according to current settings'''
        url = f"https://inventories.cs.money/5.0/load_bots_inventory/730?" \
              f"buyBonus=40&type={self.settings.get_current_type()}&" \
              f"isStore=true&limit=60&maxPrice={self.settings.get_max_price()}&" \
              f"minPrice={self.settings.get_min_price()}&offset={_offset}&withStack=true"
        print(url)
        return url

    def get_items(self, _url):
        '''get json data from GET-request'''
        ua = generate_user_agent()
        response = requests.get(url=_url, headers={'user_agent': ua})
        data = response.json()
        items = data.get('items')
        return items


    def fill_result_list(self, **kwargs):
        '''create dictionary to transfer in json file'''
        self.result.append(kwargs)

    def collect_data(self):
        '''handle data from url'''
        offset = 0
        self.result.clear()
        #When current mode is parsing, the input and buttons press from user are not handled.
        self.settings.set_current_mode(Modes.PARSING)
        while True:
            _url = self.get_url(offset)
            items = self.get_items(_url)
            #I suppose it's a better way to go through all pages, better than using loop with rang() function
            #you even no need to know how many pages there will be.
            try:
                print(f"items in this page: {len(items)}")
                for i in items:
                    if i.get('overprice') is not None and i.get('overprice') < -1 * self.settings.get_discount():
                        item_full_name = i.get('fullName')
                        item_3d = i.get('3d')
                        item_price = i.get('price')
                        item_overprice = i.get('overprice')
                        self.fill_result_list(item_full_name=item_full_name, item_3d=item_3d,
                                              item_price=item_price, item_overprice=item_overprice)
                offset = self.update_offset(offset)
            except Exception as e:
                #exception occurs when there will be absent of next page of request. Each request has 60 elements.
                #it's site limit.

                #now informtion of user will be handled.
                self.settings.set_current_mode(Modes.START)
                break

    #this function uses only on 64 line. Just wanted to separate functionality of method.
    def update_offset(self,_offset):
        '''update offset of url request. every time it should be 60'''
        _offset += General.OFFSET.value
        return _offset

    def create_file_name(self,file_prefix):
        '''update information about settings'''
        cat_id = self.settings.get_current_type()
        #format of the file's name is not perfect, I suppose it's better to use time stamp in name.
        #the name of file could be repeated in this case.
        _string = "{} - {} - {} - result.json".format(datetime.now().date(),
                                                      file_prefix,
                                                      self.settings.find_cat_name(cat_id))
        return _string

    def dump_to_file(self,file_prefix):
        '''save information to .json file'''
        filename = self.create_file_name(file_prefix)
        self.settings.set_file_name(filename)
        with open(General.FILE_WAY.value+filename, 'w', encoding='UTF-8') as file:
            json.dump(self.result, file, indent=4, ensure_ascii=False)

        #print(len(self.result))

