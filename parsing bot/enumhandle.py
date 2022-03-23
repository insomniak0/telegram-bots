from settings import Settings
from enumdata import Texts


class EnumHandle:
    def __init__(self):
        self.bot_settings :Settings = None

    def update_settings_text(self):
        '''update information about prices and discounts.'''
        #TODO: add information about current type of data.
        changed_settings_string = Texts.SETTINGS_CHANGED.value.format(self.bot_settings.get_min_price(),
                                                                      self.bot_settings.get_max_price(),
                                                                      self.bot_settings.get_discount())
        return changed_settings_string

    def set_settings(self,_settings):
        '''needs to get information about bot settings'''
        self.bot_settings = _settings

