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

import ctypes, pygame, scripts.utility.glob as glob
from scripts.ui.ui_element import UIElement, Button, Text
from scripts.utility.logger import Logger
from scripts.audio.audio import AudioUI
from scripts.ui.key_input import KeyInput
from scripts.ui.input_stream import InputStream
glob.init()

## UI Class
class WindowUI:
    """Class for handeling the window and its UI
    """    
    
    __DEFUALT_CAPTION = "New Window"
    
    __INVALID_TEXT_UPDATE = "Couldn't update text for '{elem_name}'."
    __ADDED_UI_ELEM = "UI Element '{name}' added as '{data}'."
    
    def __init__(self, 
                 win_dim: tuple[int, int] = (700, 500), 
                 caption: str = None,
                 icon: str = None,
                 b_colour: str = None,
                 framerate: int = None,
                 volume: float = 50.0):
        """Constructor for UI class

        Args:
            win_dim (tuple[int, int], optional): Window (<width>, <height>). Defaults to (700, 500).
        """        
        
        # ctypes.windll.user32.SetProcessDPIAware() ## DON'T TURN THIS ON WITH FULLSCREEN
        
        self.win_dim: tuple[int, int] = None
        self.win: pygame.Surface = None

        self.__clock = pygame.time.Clock()
        self.framerate = framerate
        
        self.__set_win(win_dim)
        self.resized: bool = False
        self.rescaled: bool = False
        self.set_caption(caption)
        
        self.b_colour = b_colour
        
        self.__ui_elems: dict[str, UIElement | Button] = {}
        
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.mouse_press: bool = False
        self.mouse_press_frames: int = 0
        self.scroll_up: bool = False
        self.scroll_down: bool = False
        
        glob.audio = AudioUI(volume)
        self.keyboard = KeyInput()
        self.input_stream = InputStream()


    def __set_win(self, win_dim: tuple[int, int]):
        """Creates a new window.

        Args:
            win_dim (tuple[int, int]): Window (<width>, <height>).
        """        

        self.win_dim = win_dim
        self.win = pygame.display.set_mode(self.win_dim, pygame.RESIZABLE)
        
        
    def set_caption(self, caption: str):
        """Sets the window caption.

        Args:
            caption (str): Window caption.
        """        
        
        if caption == None:
            pygame.display.set_caption(self.__DEFUALT_CAPTION)
        else:
            pygame.display.set_caption(caption)
            
            
    
    def __set_clock_tick(self):
        
        glob.update_delta_time()
        
        if self.framerate != None:
            self.__clock.tick(self.framerate)
            
    def get_fps(self) -> float:
        return self.__clock.get_fps()
        

    def events(self) -> bool:
        """Handles the window events, including resizing and quitting.

        Returns:
            bool: Whether the window is open.
        """
        
        self.resized = False
        self.rescaled = False
        self.scroll_down = False
        self.scroll_up = False
        
        self.keyboard.set_current_inputs()

        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.mouse_press = True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                self.mouse_press = False
                self.mouse_press_frames = 0
            
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.scroll_up = True
                
                elif event.y < 0:
                    self.scroll_down = True
                
                
            
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.VIDEORESIZE:
                self.resized = True
                
        self.input_stream.modify_text(
            self.win_dim, 
            self.keyboard.pressed_keys, 
            self.keyboard.past_pressed_keys
        )
                
        if self.mouse_press:
            self.mouse_press_frames += 1
        
        if self.resized:
            self.__resize()
            
        self.__set_clock_tick()
                
        return True
    
    
    def draw(self, 
             b_surf: tuple[pygame.Surface, tuple[int, int]] = None, 
             f_surf: tuple[pygame.Surface, tuple[int, int]] = None):
        """Draws a new frame of the window; including all its elements.
        """
        
        if self.b_colour != None:
            self.win.fill(glob.get_colour(self.b_colour))
            
        if b_surf != None:
            self.win.blit(b_surf[0], b_surf[1])
        
        self.draw_elems()
        
        if f_surf != None:
            self.win.blit(f_surf[0], f_surf[1])

        pygame.display.flip()
        
        
    def __resize(self):
        """Resizes the window, updating all its elements.
        """        
        
        self.win_dim = (self.win.get_width(), self.win.get_height())
        self.resize_elems()    
        
    
    def add_elem(self, 
                 elem_name: str, 
                 elem: UIElement | Button) -> UIElement | Button:
        
        """Adds a UI Element to be displayed on the window.

        Args:
            elem_name (str): Arbitrary name.
            elem (UIElement | Button): UI Element to be added.
        """     
                    
        if elem_name in self.__ui_elems:
            
            Logger.warn_overwritten(
                elem_name,
                self.__ui_elems[elem_name], 
                elem)
        
        self.__ui_elems[elem_name] = elem
        
        self.__ui_elems[elem_name].set_surf(self.win_dim)
        
        Logger.log_info(self.__ADDED_UI_ELEM.format(
                name = elem_name,
                data = elem))
        
        return self.__ui_elems[elem_name]
        
        
        
    def get_elem(self, elem_name: str) -> UIElement | Button:
        """Returns an UI element from an element name

        Args:
            elem_name (str): element name.

        Returns:
            UIElement | Button: The UI element.
        """        
        
        return self.__ui_elems[elem_name]

        
    def draw_elems(self):
        """Draws UI elements on the window.
        """
        
        for elem_name in self.__ui_elems:
            self.__ui_elems[elem_name].draw(self.win)
            
            
    def resize_elems(self, update_scale: bool = False):
        """Resizes UI Elements based on the window dimensions.
        """      
        
        for elem_name in self.__ui_elems:
            
            if update_scale:
                self.__ui_elems[elem_name].set_surf(self.win_dim)
            
            self.__ui_elems[elem_name].set_pos(self.win_dim)
    
    def update_text(self, 
                    elem_name: str,
                    text: str = None, 
                    font: str = None, 
                    colour: int = None):
        """
        Update the text of a UI element.

        Args:
            elem_name (str): The name of the UI element.
            text (str, optional): The new text to be set. Defaults to None.
            font (str, optional): The new font of the text. Defaults to None.
            colour (int, optional): The new colour of the text. Defaults to 
            None.
        """
        
        text_elem = self.get_elem(elem_name)
        
        if not Logger.raise_incorrect_type(
                text_elem, 
                Text, 
                self.__INVALID_TEXT_UPDATE.format(elem_name = elem_name)):
            
            text_elem.update_text(self.win_dim, 
                                  text, 
                                  font, 
                                  colour)            
    
    def is_pressed(self,
                   elem_name: str, 
                   hold: bool = False,
                   toggle: bool = False) -> bool:
        """
        Checks if a UI element is pressed.

        Args:
            elem_name (str): The name of the UI element.
            hold (bool, optional): Whether to check for a single press or a 
            continuous hold. Defaults to False.

        Returns:
            bool: True if the UI element is pressed, False otherwise.
        """

        ## Getting the UI elem
        ui_elem = self.get_elem(elem_name)
        
        
        ## Verifying whether there is an intersection
        if isinstance(ui_elem, UIElement):
            intersects = ui_elem.intersects(self.mouse_pos)
            
        elif isinstance(ui_elem, Button):
            intersects = ui_elem.intersects(self.mouse_pos, self.mouse_press, toggle)
        
        else:
            intersects = False
        
        
        ## Determining whether the button is pressed/held
        if hold:
            outcome =  intersects and self.mouse_press
        
        else:
            outcome =  intersects and self.mouse_press_frames == 1
            
            
        ## Handeling toggle buttons
        if toggle and type(ui_elem) == Button:
            if outcome:
                ui_elem.toggle()
            
            return ui_elem.toggle_state
                    
        
        ## Returning the results
        return outcome
                
                
    def set_scale(self, value: float):
        
        if value != glob.scale:
            glob.scale = value
            
            self.rescaled = True
            
            glob.set_font_scale()
            
            self.resize_elems(True)
    
   