from enumdata import Modes,Categories
class Settings:

    def __init__(self):
        self.discount = 10
        self.min_price = 100
        self.max_price = 500
        self.current_type=2
        self.current_mode: Modes = Modes.START.value
        self.filename = ""
        self.is_started = 0

    def get_is_started(self):
        return self.is_started

    def set_is_started(self,n):
        self.is_started = 1

    def get_current_mode(self):
        return self.current_mode

    def set_current_mode(self,_mode:Modes):
        self.current_mode = _mode

    def set_discount(self, _discount: int = 20):
        '''set search criteria. This discount will be used as a filter for .json file'''
        _discount = abs(int(_discount)) #abs() - discount should be > 0. int() - by <0 there is an error: _disctount is a string
        #if discount is > 100 it should be 100.
        if _discount>100:
            _discount=100

        self.discount =_discount

    def get_discount(self):
        return self.discount

    def set_min_price(self, _min_price: int = 100):
        _min_price = abs(int(_min_price)) # price should be above zero
        #min price should be < max price.
        if _min_price >= self.get_max_price():
            _min_price = self.get_max_price()

        self.min_price = _min_price

    def get_min_price(self):
        return self.min_price

    def set_max_price(self, _max_price: int = 500):
        _max_price=abs(int(_max_price)) #max price should be above zero
        #if max price < min price, it becomes a little bit higher. +10$
        if _max_price<self.get_min_price():
            _max_price=self.get_min_price()+10

        self.max_price = _max_price

    def get_max_price(self):
        return self.max_price

    def set_current_type(self,_type):
        self.current_type = _type

    def get_current_type(self):
        return self.current_type

    #TODO: Move this code to enumhanlde.
    def find_cat_id(self, _category_name,):
        '''find category id in enumdata file '''
        for n in Categories.CATEGORIES.value:
            if n.get('name') == _category_name:
                return n.get('cat_id')
        return 0

    #TODO: Move this code to enumhanlde.
    def find_cat_name(self, _category_id,):
        '''find category name in enumdata file '''
        for n in Categories.CATEGORIES.value:
            if n.get('cat_id') == _category_id:
                return n.get('name')
        return 0

    def set_file_name(self,_filename):
        self.filename = _filename

    def get_file_name(self):
        return  self.filename
