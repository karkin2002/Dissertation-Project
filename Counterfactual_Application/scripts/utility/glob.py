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

import time
from pygame import Surface, font as pyfont
from scripts.audio.audio import AudioUI
from scripts.utility.basic import is_only_type, get_first_item_of_incorrect_type
from scripts.utility.logger import Logger
from dataclasses import dataclass


def init():
    
    ## Global Colour Dictonary Variables
    global glob_colour_dict
    glob_colour_dict = {}
    
    ## Global Image Dictonary Variables
    global glob_img_dict
    glob_img_dict = {}
    
    ## Global Font Dictonary Variables
    global glob_font_dict
    glob_font_dict = {}
    
    ## Global Tag Dictonary
    global glob_tags
    glob_tags = {}
    
    global audio
    audio = None
    
    global scale
    scale = 1.0
    
    global last_delta_time, delta_time, framerate
    last_delta_time = time.time()
    delta_time = time.time() - last_delta_time
    framerate = 60
    
OVERWRITTEN = "{data_type} '{name}' overwritten from '{pre_data}' to '{post_data}'."
ADDED_TO_DICT = "{data_type} '{name}' added as '{data}'."

COLOUR = "Colour"
INVALID_COLOUR_VALUE = "Invalid colour value."
INVALID_COLOUR_NAME = "Invalid colour name."

IMG = "Image"
INVALID_IMG_SURF = "Invalid image surface."
INVALID_IMG_NAME = "Invalid image name."

FONT = "Font"
INVALID_FONT_NAME = "Invalid font name."

ADDED_TAG = "Tag '{name}' added as '{data}'."
INVALID_TAG_ID = "Invalid Tag ID."
INVALID_TAG = "Invalid Tag Object."

@dataclass     
class Tag: 
    tag_id: str
    description: str = ""
    display: bool = True


def add_colour(colour_name: str, colour: tuple[int, int, int]):
    """Adds a new colour to the global colour dictonary.

    Args:
        colour_name (str): Arbitrary name of the colour.
        colour (tuple[int, int, int]): Colour as (<red_value>, <green_value>,
        <blue_value>)
    """        
    
    if ((not Logger.raise_incorrect_type(colour, tuple, INVALID_COLOUR_VALUE)) and 
        (not Logger.raise_incorrect_len(colour, 3, INVALID_COLOUR_VALUE)) and 
        is_only_type(colour, int)):
        
        if colour_name in glob_colour_dict:
            Logger.log_warning(
                OVERWRITTEN.format(
                    data_type = COLOUR,
                    name = colour_name,
                    pre_data = glob_colour_dict[colour_name],
                    post_data = colour))
        
        glob_colour_dict[colour_name] = colour
        
        Logger.log_info(ADDED_TO_DICT.format(
            data_type = COLOUR,
            name = colour_name,
            data = colour))
    
    else:        
        Logger.raise_incorrect_type(
            get_first_item_of_incorrect_type(colour, int), 
            int,
            INVALID_COLOUR_VALUE)
            

def get_colour(colour_name: str) -> tuple[int, int, int]:
    """Returns a colour from a name

    Args:
        colour_name (str): Name of the colour.

    Returns:
        tuple[int, int, int]: Colour.
    """    
    
    if not Logger.raise_key_error(glob_colour_dict, 
                                  colour_name,
                                  INVALID_COLOUR_NAME):
        
        return glob_colour_dict[colour_name]
    



### IMAGES ----------------------------------
def add_img_surf(img_name: str, img_surf: Surface):
    """Adds a new surface to the global image dictonary.

    Args:
        img_name (str): Arbitrary name of the surface.
        img_surf (Surface): Surface to be added.
    """    
    
    if not Logger.raise_incorrect_type(img_surf, Surface, INVALID_IMG_SURF):
        
        if img_name in glob_img_dict:
            Logger.log_warning(
                OVERWRITTEN.format(
                    data_type = "Image",
                    name = img_name,
                    pre_data = glob_img_dict[img_name],
                    post_data = img_surf))
        
        glob_img_dict[img_name] = img_surf
        
        Logger.log_info(ADDED_TO_DICT.format(
            data_type = IMG,
            name = img_name,
            data = img_surf))
        
        
def get_img_surf(img_name: str) -> Surface:
    """Reutnrs a surface from a name

    Args:
        img_name (str): Name of the surface.

    Returns:
        Surface: Surface.
    """    
    
    if not Logger.raise_key_error(glob_img_dict, 
                                  img_name,
                                  INVALID_IMG_NAME):
    
        return glob_img_dict[img_name]

def get_img_dim(img_name: str) -> tuple[int, int]:
    """
    Get the dimensions of an image.
    
    Args:
        img_name (str): The name of the image.
    
    Returns:
        tuple[int, int]: A tuple containing the width and height of the image.
    """
    
    img_surf = get_img_surf(img_name)
    return (img_surf.get_width(), img_surf.get_height())
### ------------------------------------------
    



### FONTS -------------------------
def add_font(font_name: str, font: str, size: int):
    """
    Add a font to the global font dictionary.
    
    Parameters:
        font_name (str): Arbitrary font name.
        font (str): The name of the font, or the filepath of the font.
        size (int): The size of the font.
    """
    
    if font in pyfont.get_fonts():
        font_format = pyfont.SysFont(font, round(size * scale))
    else:
        font_format = pyfont.Font(str(font), round(size * scale))
    
    if font_name in glob_font_dict:
        Logger.log_warning(
            OVERWRITTEN.format(
                data_type = FONT,
                name = font_name,
                pre_data = glob_font_dict[font_name],
                post_data = font_format))
        
    glob_font_dict[font_name] = (font, size, font_format)
        
    Logger.log_info(ADDED_TO_DICT.format(
        data_type = FONT,
        name = font_name,
        data = font_format))


def get_font(font_name: str) -> pyfont.Font:
    """
    Returns a font from the global font dictonary.

    Parameters:
        font_name (str): Arbitrary font name.

    Returns:
        Font: The font object.
    """
    
    if not Logger.raise_key_error(glob_font_dict, 
                                  font_name,
                                  INVALID_FONT_NAME):
        
        return glob_font_dict.get(font_name)[2]
    
    
def set_font_scale():
    for font_name in glob_font_dict:
        font = glob_font_dict[font_name][0]
        size = glob_font_dict[font_name][1]
        add_font(font_name, font, size)
        
        
### ------------------------------------



### TAGS ---------------------
def add_tag(tag: Tag):
    """Adds a tag to the global tag dictonary.

    Args:
        tag (Tag): Tag object.
    """
    
    if not Logger.raise_incorrect_type(tag.tag_id, str, INVALID_TAG_ID):
        if not Logger.raise_incorrect_type(tag, Tag, INVALID_TAG):
            if tag.tag_id in glob_tags:
                Logger.log_warning(
                    OVERWRITTEN.format(
                        data_type=Tag, 
                        name = str(tag.tag_id), 
                        pre_data = glob_tags[tag.tag_id], 
                        post_data = tag
                    ))
            
            glob_tags[tag.tag_id] = tag
            
            Logger.log_info(ADDED_TAG.format(name = str(tag.tag_id), data = glob_tags[tag.tag_id]))
        

def get_tag(tag_id: str) -> Tag:
    """Returns a tag from the global tag dictonary.

    Args:
        tag_id (str): Tag ID.

    Returns:
        Tag: Tag object.
    """
    
    return glob_tags[tag_id]


def is_tag(tag_id: str) -> bool:
    """Returns whether a tag exists in the global tag dictonary.

    Args:
        tag_id (str): Tag ID.

    Returns:
        bool: Whether the tag exists.
    """
    
    return tag_id in glob_tags
### -------------------------------------


### Delta time ---------------------------

def update_delta_time():
    global last_delta_time, delta_time, framerate
    delta_time = time.time() - last_delta_time
    delta_time *= framerate
    last_delta_time = time.time()

### -------------------------------------