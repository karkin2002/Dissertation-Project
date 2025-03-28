__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

"""
This file is part of Arctic Engine Project by Kaya Arkin. For more information,
look at the README.md file in the root directory, or visit the
GitHub Repo: https://github.com/karkin2002/Arctic-Engine.
"""


from scripts.utility.logger import Logger
from scripts.utility.basic import load_json_file
import pygame

class KeyInput:
    KEYBIND_JSON_PATH = r"config/ui/keybind.json"
    
    KEYBIND_NOT_EXIST_TEXT = "Custom keybind name does not exist."
    KEYCODE_NOT_EXIST_TEXT = "Keycode does not exist."
    
    def __init__(self):
        self.__keybind_dict: dict[str, str] = load_json_file(KeyInput.KEYBIND_JSON_PATH)
        
        self.__current_inputs = pygame.key.get_pressed()
        self.__past_input = self.__current_inputs
        self.pressed_keys = []
        self.past_pressed_keys = self.pressed_keys
        
        
    def __get_key_code(self, keybind_name: str) -> int:
        
        if not Logger.raise_key_error(self.__keybind_dict,
                                      keybind_name,
                                      KeyInput.KEYBIND_NOT_EXIST_TEXT,
                                      False):
                
            return pygame.key.key_code(self.__keybind_dict[keybind_name])
        
        else:
            return -1
        
    def set_current_inputs(self):
        self.__past_input = self.__current_inputs
        self.__current_inputs = pygame.key.get_pressed()
        self.__set_pressed_keys()
        
        
    def is_pressed(self, keybind_name: str, hold = False) -> bool:
        
        keycode = self.__get_key_code(keybind_name)
        
        if not Logger.raise_index_error(self.__current_inputs,
                                      keycode,
                                      KeyInput.KEYCODE_NOT_EXIST_TEXT,
                                      False):
            
            if hold:
                return self.__current_inputs[self.__get_key_code(keybind_name)]
            
            else:
                return (self.__current_inputs[self.__get_key_code(keybind_name)] and
                        not self.__past_input[self.__get_key_code(keybind_name)])
            
        
        return False
    
    def __set_pressed_keys(self):

        self.past_pressed_keys = self.pressed_keys
        self.pressed_keys = []
        for key_code in range(len(self.__current_inputs)):
            if self.__current_inputs[key_code]:
                try:
                    key_name = pygame.key.name(key_code)
                    self.pressed_keys.append(key_name)
                except ValueError:
                    # Ignore invalid key codes
                    pass
            
        
        