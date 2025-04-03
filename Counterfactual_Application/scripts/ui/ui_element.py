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

import pygame
from pygame import font as pyfont
from scripts.utility.logger import Logger
from abc import abstractmethod
import scripts.utility.glob as glob
glob.init()


## UI Element Class
class UIElement:
    
    __TAGS_TEXT = "UI Element '{object}' has the following tags: {tags}."
    __INVALID_TAGS = "Invalid tag."
    
    ## Alignment Static Variables.
    ALIGN_TOP_KW = "align_top"
    ALIGN_RIGHT_KW = "align_right"
    ALIGN_BOTTOM_KW = "align_bottom"
    ALIGN_LEFT_KW = "align_left"
    
    DEFAULT_ALIGN_DICT = {
        ALIGN_TOP_KW: False,
        ALIGN_RIGHT_KW: False,
        ALIGN_BOTTOM_KW: False,
        ALIGN_LEFT_KW: False}
    
    DEFAULT_DIM = (100, 100)

    def __init__(self, 
                 dim: tuple[int, int], 
                 offset: tuple[int, int] = (0, 0), 
                 alpha: int = 255,
                 centered: bool = True, 
                 display: bool = True,
                 tags: list[str] = [],
                 **align_args: dict[str, bool]):
        
        """Constuctor for UIElement class.

        Args:
            dim (tuple[int, int]): Dimensions as (<width>, <height>).
            offset (tuple[int, int], optional): Offset in pixels from it's 
            original alignment. Defaults to (0, 0).
            centered (bool, optional): Whether the element should be drawn from 
            the center of its width/height. Defaults to True.
            align_args (dict[str, bool], optional): Specifies which side of the
            surface the UI Element should align to. Options are align_top=<bool>, 
            align_right=<bool>, align_bottom=<bool>, align_left=<bool>.
        """      
          
        self.dim: tuple[int, int] = dim
        self.offset: tuple[int, int] = offset
        self.alignment = self.DEFAULT_ALIGN_DICT.copy()
            
        self.__set_align(**align_args)
        self.__centered = centered
        
        self.__pos = [0, 0]
        
        self.__alpha = alpha
        self.__display = display
        
        self.__surf = None
        self.__in_surf_bounds = True
        
        self.tags = []
        
        self.__set_tags(tags)
    
    @abstractmethod
    def set_surf(self, surf_dim: tuple[int, int]):
        pass
        
    def set_display(self, display: bool):
        """Sets whether the UIElement should be displayed.

        Args:
            display (bool): True to display the UIElement, False to hide it.
        """
        self.__display = display
        
        
    def get_display(self) -> bool:
        """Returns whether the UIElement is being displayed.

        Returns:
            bool: Whether it's being displayed.
        """
        return self.__display
    
    def __set_tags(self, tags: list[str]):
        
        if tags:
            
            if not Logger.raise_incorrect_type(tags, list, self.__INVALID_TAGS):
                
                for tag_id in tags:  
                    
                    if not glob.is_tag(tag_id):
                        glob.add_tag(glob.Tag(tag_id))
                    
                    self.tags.append(tag_id)
              
            Logger.log_info(self.__TAGS_TEXT.format(object=self, tags = self.tags))
        
        
        
    def __set_align(self, **align_args: dict[str, bool]):
        """Sets the alignment for the UI Element.

        Args:
            align_args (dict[str, bool], optional): Specifies which side of the
            surface the UI Element should align to. Options are align_top=<bool>, 
            align_right=<bool>, align_bottom=<bool>, align_left=<bool>.
        """        
        
        for align_name in align_args:
            if not Logger.raise_incorrect_type(align_args[align_name], bool):
                if align_name in self.alignment:
                    self.alignment[align_name] = align_args[align_name]          
                
                
    def _create_surf(self, surf_dim: tuple[int, int], surf: pygame.Surface):
        """Sets the UI Elements surface. 

        Args:
            surf_dim (tuple[int, int]): (<width>, <height>) of the surface to be 
            drawn on.
            surf (Surface): The surface to be set.
        """        
        
        self.__surf = surf
        self.dim = (surf.get_width(), surf.get_height())
        self.set_pos(surf_dim)
        
        
        
    def draw(self, surf: pygame.Surface):
        """Draws the UIElement on a surface.

        Args:
            surf (Surface): Surface to be drawn on.
        """   
            
        if self.is_displayed():
            surf.blit(self.__surf, self.__pos)
            
            
    def is_displayed(self) -> bool:
        """Returns whether the UIElement is being displayed.

        Returns:
            bool: Whether it's being displayed.
        """
        
        if self.tags:
            if not any(glob.get_tag(tag_id).display for tag_id in self.tags):
                return False
        
        return (self.__display and 
                self.__alpha > 0 and 
                self.__surf != None and 
                self.__in_surf_bounds)
    
    
    def __set_in_surf_bounds(self, surf_dim: tuple[int, int]):
        """Sets whether the UIElement is visible on the surface.

        Args:
            surf_dim (tuple[int, int]): (<width>, <height>) of the surface to be 
            drawn on.
        """        
        
        self.__in_surf_bounds = (self.__pos[0] + self.dim[0] >= 0 and
                                 self.__pos[0] <= surf_dim[0] and
                                 self.__pos[1] + self.dim[1] >= 0 and
                                 self.__pos[1] <= surf_dim[1])
            
        
    def set_pos(self, surf_dim: tuple[int, int]):
        """Sets the position for the UI Element to be displayed on a surface.

        Args:
            surf_dim (tuple[int, int]): (<width>, <height>) of the surface to be 
            drawn on.
        """        
        
        for i in range(2):
            
            half_surf_len = round(surf_dim[i] / 2)
            
            offset = self.offset[i] * glob.scale
            
            if i == 0 and not (self.alignment[self.ALIGN_RIGHT_KW] and self.alignment[self.ALIGN_LEFT_KW]):
                
                if self.alignment[self.ALIGN_RIGHT_KW]:
                    offset += half_surf_len
                
                elif self.alignment[self.ALIGN_LEFT_KW]:
                    offset -= half_surf_len
                    
            if i == 1 and not (self.alignment[self.ALIGN_TOP_KW] and self.alignment[self.ALIGN_BOTTOM_KW]):
                
                if self.alignment[self.ALIGN_BOTTOM_KW]:
                    offset += half_surf_len
                
                elif self.alignment[self.ALIGN_TOP_KW]:
                    offset -= half_surf_len
        
            if self.__centered:
                offset -= round(self.dim[i] / 2)
            
            self.__pos[i] = half_surf_len + offset
            
        self.__set_in_surf_bounds(surf_dim)
        
        
    def intersects(self, pos: tuple[int, int]) -> bool:
        """Returns whether pos is within the ui element.

        Args:
            pos (tuple[int, int]): The position to check.

        Returns:
            bool: True if pos is within the object's dimensions, False 
            otherwise.
        """
        
        return (self.__pos[0] <= pos[0] <= self.__pos[0] + self.dim[0] and 
                self.__pos[1] <= pos[1] <= self.__pos[1] + self.dim[1])
                    

class Box(UIElement):
    def __init__(self,
                 box_dim: tuple[int, int],
                 colour: str,
                 outline_width: int = 0,
                 outline_colour: str = None,
                 border_radius: int = 0,
                 offset: tuple[int, int] = (0, 0),
                 alpha: int = 255,
                 centered: bool = True,
                 display: bool = True,
                 tags: list[str] = [],
                 **align_args: dict[str, bool]):
        
        super().__init__(
            self.DEFAULT_DIM,
            offset,
            alpha,
            centered,
            display,
            tags,
            **align_args
        )
        
        self.original_box_dim = box_dim
        self.box_dim = self.original_box_dim
        self.colour = colour
        self.border_radius = border_radius
        self.outline_width = outline_width
        self.outline_colour = outline_colour
        
        
    def set_surf(self, surf_dim: tuple[int, int]):

        rect_dim = (self.box_dim[0] * glob.scale, self.box_dim[1] * glob.scale)
        surface = pygame.Surface(rect_dim, pygame.SRCALPHA)

        pygame.draw.rect(
            surface,
            glob.get_colour(self.colour),
            [0, 0, rect_dim[0], rect_dim[1]],
            border_radius = round(self.border_radius * glob.scale)
        )

        if self.outline_width > 0:
            pygame.draw.rect(
                surface,
                glob.get_colour(self.outline_colour),
                [0, 0, rect_dim[0], rect_dim[1]],
                self.outline_width,
                border_radius = round(self.border_radius * glob.scale)
            )
        
        self._create_surf(
            surf_dim, 
            surface)


class Text(UIElement):
    
    def __init__(self, 
                 text: str,
                 font: str,
                 colour: str,
                 offset: tuple[int, int] = (0, 0),
                 alpha: int = 255,
                 centered: bool = True,
                 display: bool = True,
                 tags: list[str] = [],
                 **align_args: dict[str, bool]):       
        
        super().__init__(
            self.DEFAULT_DIM,
            offset,
            alpha,
            centered,
            display,
            tags,
            **align_args
        )
        
        self.text = text
        self.font = font
        self.colour = colour
        
    def createText(text: str, 
                   font: str, 
                   colour: tuple) -> pygame.Surface:
        """Creates a surface with text on it.

        Args:
            text (str): Text to be drawn on the surface.
            font (str): Font of the text.
            colour (tuple): Colour of the text.

        Returns:
            pygame.Surface: Surface with text.
        """

        message = glob.get_font(font).render(text, True, colour)

        return message
        
    def set_surf(self, surf_dim: tuple[int, int]):

        self._create_surf(
            surf_dim, 
            Text.createText(
                self.text,
                self.font, 
                glob.get_colour(self.colour)
            )
        )
        
        
    def update_text(self, 
                        surf_dim: tuple[int, int],
                        text: str = None, 
                        font: str = None, 
                        colour: int = None):

            
            update = False
            
            if text != None and text != self.text: 
                self.text = text
                update = True
            
            if font != None and font != self.font: 
                self.font = font
                update = True
            
            if colour != None and colour != self.colour: 
                self.colour = colour
                update = True
            
            if update:
                self.set_surf(surf_dim)
                
                
                
class TextBox(Text):
    def __init__(self,
                 box_dim: tuple[int, int],
                 text: str,
                 font: str,
                 colour: str,
                 box_colour: str = None,
                 outline_width: int = 0,
                 outline_colour: str = None,
                 border_radius: int = 0,
                 offset: tuple[int, int] = (0, 0),
                 alpha: int = 255,
                 centered: bool = True,
                 display: bool = True,
                 tags: list[str] = [],
                 **align_args: dict[str, bool]):
        
        super().__init__(
            text,
            font,
            colour,
            offset,
            alpha,
            centered,
            display,
            tags,
            **align_args
        )
        
        self.box_dim = box_dim
        self.box_colour = box_colour
        self.outline_width = outline_width
        self.outline_colour = outline_colour
        self.border_radius = border_radius
        
        
    def set_surf(self, surf_dim: tuple[int, int]):
        new_edge_box_dim = ((self.box_dim[0] + self.outline_width) * glob.scale, (self.box_dim[1] + self.outline_width) * glob.scale)
        new_box_dim = (self.box_dim[0] * glob.scale, self.box_dim[1] * glob.scale)

        surface = pygame.Surface(new_edge_box_dim, pygame.SRCALPHA)

        if self.box_colour != None:
            pygame.draw.rect(
                surface,
                glob.get_colour(self.box_colour),
                [0, 0, new_edge_box_dim[0], new_edge_box_dim[1]],
                border_radius = round(self.border_radius * glob.scale)
            )

            if self.outline_width > 0:
                pygame.draw.rect(
                    surface,
                    glob.get_colour(self.outline_colour),
                    [0, 0, new_edge_box_dim[0], new_edge_box_dim[1]],
                    self.outline_width,
                    border_radius = round(self.border_radius * glob.scale)
                )

        font = glob.get_font(self.font)
        
        words = self.text.split(' ')
        space_width, _ = font.size(' ')
        x, y = 0, 0
        
        # Ellipsis size
        ellipsis_width, ellipsis_height = font.size('...')
        
        for i, word in enumerate(words):
            word_width, word_height = font.size(word)
            
            # If the word doesn't fit on the current line, move to the next line
            if x + word_width > new_box_dim[0]:
                x = 0
                y += word_height
            
            # If the next word or ellipsis won't fit in the box, stop and add "..."
            next_word_width, _ = font.size(words[i + 1]) if i + 1 < len(words) else (0, 0)
            if (
                y + word_height > new_box_dim[1] or  # Text exceeds box height
                (x + word_width + next_word_width + space_width > new_box_dim[0] and y + word_height + ellipsis_height > new_box_dim[1])  # Not enough room for next word or "..."
            ):
                # Only add ellipsis if it fits in the current line
                if x + ellipsis_width <= new_box_dim[0] and y + ellipsis_height <= new_box_dim[1]:
                    surface.blit(
                        Text.createText('...', self.font, glob.get_colour(self.colour)), (x + (self.outline_width * glob.scale), y + (self.outline_width * glob.scale))
                    )
                break
            
            # Draw the word if there's still space
            surface.blit(
                Text.createText(word, self.font, glob.get_colour(self.colour)), (x + (self.outline_width * glob.scale), y + (self.outline_width * glob.scale))
            )
            x += word_width + space_width

        self._create_surf(
            surf_dim, 
            surface
        )
            
            
        
        
    
                

        


class Image(UIElement):
    
    def __init__(self, 
                 img_name: str,
                 scale: float = 1.0,
                 offset: tuple[int, int] = (0, 0),
                 alpha: int = 255,
                 centered: bool = True,
                 display: bool = True,
                 tags: list[str] = [],
                 **align_args: dict[str, bool]):
        
        super().__init__(
            self.DEFAULT_DIM,
            offset,
            alpha,
            centered,
            display,
            tags,
            **align_args
        )
        
        self.img_name = img_name
        self.scale = scale
        
        
    def set_surf(self, surf_dim: tuple[int, int]):
        
        img_surf = glob.get_img_surf(self.img_name)
        
        if self.scale != 1:
            img_surf = pygame.transform.scale_by(
                img_surf, 
                self.scale * glob.scale)
        
        self._create_surf(surf_dim, img_surf)
        
        
        
        
class Button:
    
    UNPRESS = "unpress"
    HOVER = "hover"
    PRESS = "press"
    __INVALID_STATE = f"State name doesn't match predefined states: '{UNPRESS}', '{HOVER}', '{PRESS}'."
    __INVALID_TYPE = "Invalid state added to button."
    
    __TOGGLE_STATES = {
        UNPRESS: False,
        HOVER: False,
        PRESS: True
    }
    
    
    def __init__(self, 
                 unpress_elem: UIElement,
                 hover_elem: UIElement = None,
                 press_elem: UIElement = None,
                 hover_audio: tuple[str, str] = None,
                 press_audio: tuple[str, str] = None,
                 defualt_toggle_state: bool = False,
                 display: bool = True):
        
        self.states = {
            self.UNPRESS: unpress_elem,
            self.HOVER: hover_elem,
            self.PRESS: press_elem
        }
        
        self.__audio = {
            self.HOVER: hover_audio,
            self.PRESS: press_audio
        }

        for state in self.states.values():
            if state != None:
                state.set_display(False)
        
        self.current_state = self.UNPRESS
        
        self.set_display(display)
        
        self.toggle_state = defualt_toggle_state
        


    def set_display(self, display: bool):
        """Sets whether the button should be displayed.

        Args:
            display (bool): The display value to set.
        """
        
        self.__display = display
        self.states[self.current_state].set_display(display)
                    

    def get_display(self) -> bool:
        """Returns whether the Button is being displayed.

        Returns:
            bool: Whether it's being displayed.
        """
        return self.__display
        
    
    def set_state_ui_elem(self, **ui_elements: dict[str, UIElement]):
        
        for state_name in ui_elements:
            
            if not Logger.raise_key_error(
                self.states, state_name, self.__INVALID_STATE):
                
                if not Logger.raise_incorrect_type(
                    ui_elements[state_name], UIElement, self.__INVALID_TYPE):
                
                    self.states[state_name] = ui_elements[state_name]
                    
                    
    def __play_state_audio(self, state_name: str):
        
        if state_name in self.__audio:
            
            audio_data = self.__audio[state_name]
            
            if audio_data != None:
                glob.audio.play(audio_data[0], audio_data[1])
        
                    
    
    def set_curent_state(self, state_name: str):
        """Sets the current state of the button.

        Args:
            state_name (str): State name, predefined within Button class.
        """        
        
        if self.current_state != state_name:
            if not Logger.raise_key_error(
                self.states, state_name, self.__INVALID_STATE):
                
                if self.states[state_name] != None:
                    
                    self.toggle_state = self.__TOGGLE_STATES[state_name]
                    
                    self.states[self.current_state].set_display(False)
                    self.current_state = state_name
                    if self.__display:
                        self.states[self.current_state].set_display(True)
                        
                self.__play_state_audio(state_name)
            
        
        
    def set_surf(self, surf_dim: tuple[int, int]):
        for state_name in self.states:
            if self.states[state_name] != None:
                self.states[state_name].set_surf(surf_dim)
        
        
    def draw(self, surf: pygame.Surface):
        if self.states[self.current_state] != None:
            self.states[self.current_state].draw(surf)
        
    
    def set_pos(self, surf_dim: tuple[int, int]):
        for state_name in self.states:
            if self.states[state_name] != None:
                self.states[state_name].set_pos(surf_dim)
                
    
    def __is_states_displayed(self) -> bool:
        """
        Check if at least one state is displayed.

        Returns:
            bool: True if at least one state is displayed, False otherwise.
        """
        return any(state.is_displayed() for state in self.states.values() if state is not None)
                

    def intersects(self, pos: tuple[int, int], press: bool = False, toggle: bool = False) -> bool:
        """
        Checks if the UI element intersects a given position.

        Args:
            pos (tuple[int, int]): The position of the click.
            press (bool, optional): The press state of the click. Defaults to 
            False.

        Returns:
            bool: True if the UI element is pressed, False otherwise.
        """
        
        if (self.__display and 
            self.__is_states_displayed() and 
            self.states[self.UNPRESS].intersects(pos)):
            
            if press:
                if not toggle:
                    self.set_curent_state(self.PRESS)
                    
            
            elif self.states[self.HOVER] != None:
                    self.set_curent_state(self.HOVER)
            
            else:
                if not toggle:
                    self.set_curent_state(self.UNPRESS)
            
            return True
        
        
        if toggle and self.toggle_state:
            self.set_curent_state(self.PRESS)
        else:
            self.set_curent_state(self.UNPRESS)
        
        return False
    
    
    def toggle(self):
        """
        Toggles the state of the UI element.

        If the toggle state is True, sets the current state to 'PRESS'.
        If the toggle state is False, sets the current state to 'UNPRESS'.
        """
        
        self.toggle_state = not self.toggle_state
        
        if self.toggle_state:
            self.set_curent_state(self.PRESS)
        
        else:
            self.set_curent_state(self.UNPRESS)
            
