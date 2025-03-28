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
from scripts.ui.ui_element import Text
import pygame

class InputStream:
    
    __SPECIAL_CHAR_MAP = {
        '1': '!',
        '2': '@',
        '3': '#',
        '4': '$',
        '5': '%',
        '6': '^',
        '7': '&',
        '8': '*',
        '9': '(',
        '0': ')',
        '-': '_',
        '=': '+',
        '[': '{',
        ']': '}',
        '\\': '|',
        ';': ':',
        "'": '"',
        ',': '<',
        '.': '>',
        '/': '?'
    }
    
    __INVALID_TEXTUAL_UI_ELEMENT = "Invalid UI Element for input stream."
    __INPUT_STREAM_STARTED = "Input stream started."
    __INPUT_STREAM_ENDED = "Input stream ended."
    
    def __init__(self):
                
        self.__input_stream_ui_elem: Text = None
        self.input_stream: bool = False
        
        
    def set_input_stream(self, textual_ui_element: Text):
        if isinstance(textual_ui_element, Text):
            self.__input_stream_ui_elem = textual_ui_element
            self.input_stream = True
            Logger.log_info(self.__INPUT_STREAM_STARTED)
        
        else:
            Logger.raise_incorrect_type(
                textual_ui_element, 
                Text,
                self.__INVALID_TEXTUAL_UI_ELEMENT
            )
            
            
    def end_input_stream(self):
        self.input_stream = False
        self.__input_stream_ui_elem = None
        Logger.log_info(self.__INPUT_STREAM_ENDED)
        
        
    def modify_text(self, surf_dim: tuple[int, int], input: list[str], past_input: list[str]):
        if input != past_input and self.input_stream:
            # Find the first new key that wasn't in the past input
            new_keys = list(set(input) - set(past_input))
            if new_keys:
                key_name = new_keys[0]  # Take the first new key
                
                key_value = pygame.key.key_code(key_name)
                new_text = self.__input_stream_ui_elem.text
                
                if key_value == pygame.K_SPACE:
                    new_text += " "
                elif key_value == pygame.K_BACKSPACE:
                    new_text = new_text[:-1]
                elif key_value == pygame.K_RETURN:
                    new_text += "\n"
                elif key_value == pygame.K_TAB:
                    new_text += "\t"
                elif key_value == pygame.K_ESCAPE:
                    self.end_input_stream()
                    return
                else:
                    # Check for shift or caps lock
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_SHIFT:
                        # Try to get special character if shift is held
                        new_text += self.__SPECIAL_CHAR_MAP.get(key_name, key_name.upper())
                    elif mods & pygame.KMOD_CAPS:
                        new_text += key_name.upper()
                    else:
                        new_text += key_name
                
                self.__input_stream_ui_elem.update_text(surf_dim, new_text)