from scripts.ui.ui import WindowUI
from scripts.ui.ui_element import Text, TextBox, Image, Button, Box
import pygame, scripts.utility.glob as glob
from scripts.utility.logger import Logger
import tkinter as tk
from tkinter import filedialog
from custom.scripts.text_box import TextBoxUIElem, set_dim_based_on_win_dim
from custom.scripts.pre_treained_llm import PreTrainedLLM
from custom.scripts.counterfactual_generator import CounterfactualGenerator
from scripts.utility.glob import Tag


class MainUI:
    
    TITLE_FONT_PATH = r"static\fonts\example_font_title.ttf"
    REGULAR_FONT_PATH = r"static\fonts\example_font_regular.ttf"
    BOLD_FONT_PATH = r"static\fonts\example_font_bold.ttf"
    
    WHITE = "WHITE"
    BLACK = "BLACK"
    BG_COLOUR = "BG"
    WHITE_TEXT = "WHITE_TEXT"
    BLACK_TEXT = "BLACK_TEXT"
    BUTTON_TEXT_HOVER = "BUTTON_TEXT_HOVER"
    BUTTON_TEXT = "BUTTON_TEXT"
    TEXT_BOX_BG = "TEXT_BOX_BG"
    LOADING_BAR_BOX = "LOADING_BAR_BOX"
    
    TITLE_FONT = "TITLE_FONT"
    PG_FONT_REGULAR = "PG_FONT_REGULAR"
    PG_FONT_BOLD = "PG_FONT_BOLD"
    BUTTON_FONT = "BUTTON_FONT"
    BUTTON_FONT_HOVER = "BUTTON_FONT_HOVER"
    TEXT_BOX_TITLE_FONT = "TEXT_BOX_TITLE_FONT"
    
    TITLE = "title"
    __TITLE_TEXT = "LLM Counterfactual Explanation" 
    __TITLE_OFFSET = (40, 20)
    
    EXPLANATION = "EXPLANATION"
    __EXPLANATION_TEXT = "As part of \"Exploratory Research on Explainable LLMs (Airbus AI Research)\", this program experiments with counterfactuals as an explability method for LLMs."
    __EXPLANATION_OFFSET = (40, 120)
    __EXPLANATION_DIM = (40, 120)
    
    UPLOAD = "UPLOAD"
    __UPLOAD_OFFSET = (160, 280)
    
    UPLOAD_TEXT= "UPLOAD_TEXT"
    __UPLOAD_TEXT_OFFSET = (295, 262)
    DEFAULT_UPLOAD_TEXT = ":   None"
    LOADED_UPLOAD_TEXT = ":   \"{llm_file_path}\""
    
    __SCROLL_SPEED = 200
    
    __LOADING_BAR = "LOADING_BAR"
    __LOADING_BAR_BOX = "LOADING_BAR_BOX"
    __LOADING_BAR_BOX_OFFSET = (0, 0)
    __LOADING_BAR_BOX_DIM = (825, 200)
    __LOADING_BAR_TEXT = "LOADING_BAR_TEXT"
    __LOADING_BAR_TEXT_OFFSET = (0, 0)
    LOADING_TEXT = "Generating Counterfactuals..."
    
    def __init__(self, window: WindowUI):
        
        glob.add_colour(self.WHITE, (255, 255, 255))
        glob.add_colour(self.BLACK, (0, 0, 0))
        
        glob.add_colour(self.BG_COLOUR, (24, 24, 24))
        glob.add_colour(self.WHITE_TEXT, (240, 246, 252))
        glob.add_colour(self.BLACK_TEXT, (20, 20, 20))
        glob.add_colour(self.BUTTON_TEXT_HOVER, (40, 100, 150))
        glob.add_colour(self.BUTTON_TEXT, (180, 225, 255))
        glob.add_colour(self.TEXT_BOX_BG, (49, 49, 49))
        glob.add_colour(self.LOADING_BAR_BOX, (34, 34, 34))
        
        glob.add_font(self.TITLE_FONT, self.TITLE_FONT_PATH, 60)
        glob.add_font(self.PG_FONT_REGULAR, self.REGULAR_FONT_PATH, 30)
        glob.add_font(self.PG_FONT_BOLD, self.BOLD_FONT_PATH, 30)
        glob.add_font(self.BUTTON_FONT, self.BOLD_FONT_PATH, 35)
        glob.add_font(self.BUTTON_FONT_HOVER, self.BOLD_FONT_PATH, 35)
        glob.add_font(self.TEXT_BOX_TITLE_FONT, self.TITLE_FONT_PATH, 35)
        
        glob.add_img_surf("button_press", pygame.image.load(r"custom\images\button_press.png"))
        glob.add_img_surf("button_unpress", pygame.image.load(r"custom\images\button_unpress.png"))
        glob.add_img_surf("button_warning", pygame.image.load(r"custom\images\button_warning.png"))
        glob.add_img_surf("submit_unpress", pygame.image.load(r"custom\images\submit_unpress.png"))
        glob.add_img_surf("submit_press", pygame.image.load(r"custom\images\submit_unpress.png"))
        
        self.page_elements = []
        self.input_text_box = None
        self.output_text_box = None
        
        self.pixels_scrolled = 0
        
        self.llm = PreTrainedLLM()
        
        self.setup_title(window)
        self.setup_upload(window)
        self.__setup_user_input(window)
        self.__setup_loading_bar(window)
    
        
    def select_folder():
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        folder_path = filedialog.askdirectory()
        if folder_path:
            print(f"Selected folder: {folder_path}")
        root.destroy()
        
        return folder_path
    
    def setup_title(self, window: WindowUI):
        
        ## TITLE
        self.page_elements.append(window.add_elem(
            self.TITLE,
            Text(
                self.__TITLE_TEXT,
                self.TITLE_FONT,
                self.WHITE_TEXT,
                self.__TITLE_OFFSET,
                centered = False,
                align_top = True,
                align_left = True
            )
        ))
        
        ## EXPLANATION TEXT
        self.page_elements.append(window.add_elem(
            self.EXPLANATION,
            TextBox(
                (300, 300),
                None,
                self.__EXPLANATION_TEXT,
                self.PG_FONT_REGULAR,
                self.WHITE_TEXT,
                self.__EXPLANATION_OFFSET,
                centered = False,
                align_top = True,
                align_left = True
            )
        ))
        
    def setup_upload(self, window: WindowUI):
        
        ## UPLOAD BUTTON
        self.page_elements.append(window.add_elem(
            self.UPLOAD,
            Button(
                Text(
                    "[Upload LLM]",
                    self.BUTTON_FONT,
                    self.BUTTON_TEXT,
                    offset=self.__UPLOAD_OFFSET,
                    centered=True,
                    align_top = True,
                    align_left = True
                ),
                Text(
                    "[ Upload LLM ]",
                    self.BUTTON_FONT_HOVER,
                    self.BUTTON_TEXT_HOVER,
                    offset=self.__UPLOAD_OFFSET,
                    centered=True,
                    align_top = True,
                    align_left = True
                )
            )
        ))
        
        ## UPLOAD TEXT
        self.page_elements.append(window.add_elem(
            self.UPLOAD_TEXT,
            Text(
                self.DEFAULT_UPLOAD_TEXT,
                self.PG_FONT_BOLD,
                self.WHITE_TEXT,
                offset=self.__UPLOAD_TEXT_OFFSET,
                centered=False,
                align_top = True,
                align_left = True
            )
        ))
        
    
    def __handel_scroll(self, window: WindowUI):
        scroll = 0
        
        if window.scroll_up:
            if self.pixels_scrolled < 0:
                scroll = self.__SCROLL_SPEED * glob.delta_time
                
        elif window.scroll_down:
            scroll = -self.__SCROLL_SPEED * glob.delta_time
            
        if scroll != 0:
            self.pixels_scrolled += scroll

            for elem in self.page_elements:
                if type(elem) == Button:
                    for button_key in elem.states:
                        button_elem = elem.states[button_key]
                        if button_elem != None:
                            button_elem.offset = (button_elem.offset[0], button_elem.offset[1] + scroll)
                            button_elem.set_pos(window.win_dim)
                else:
                    elem.offset = (elem.offset[0], elem.offset[1] + scroll)
                    elem.set_pos(window.win_dim)
        
        
        
        
    def __setup_user_input(self, window: WindowUI):
        
        self.input_text_box = TextBoxUIElem(self.page_elements, window, "LLM_INPUT", (40, 360), "LLM Input")
        
        self.output_text_box = TextBoxUIElem(self.page_elements, window, "LLM_OUTPUT", (40, 730), "LLM Output", False)
        
    
    def __setup_loading_bar(self, window: WindowUI):
        glob.add_tag(Tag(self.__LOADING_BAR, "Loading Bar", False))
        
        window.add_elem(
            self.__LOADING_BAR_BOX,
            Box(
                self.__LOADING_BAR_BOX_DIM,
                self.__LOADING_BAR_BOX,
                self.__LOADING_BAR_BOX_OFFSET,
                tags = [self.__LOADING_BAR]
            )
        )
        
        window.add_elem(
            self.__LOADING_BAR_TEXT,
            Text(
                self.LOADING_TEXT.format(percentage=0),
                self.BUTTON_FONT,
                self.WHITE_TEXT,
                self.__LOADING_BAR_TEXT_OFFSET,
                tags = [self.__LOADING_BAR]
            )
        )
        
        
        
        
    
    def handle_inputs(self, window: WindowUI, run_first_time: bool):
        
        if window.is_pressed(self.UPLOAD):
            folder_path = MainUI.select_folder()
            window.get_elem(self.UPLOAD_TEXT).update_text(window.win_dim, self.LOADED_UPLOAD_TEXT.format(llm_file_path=folder_path))
            self.llm.set_model_folder_path(folder_path)
            
        set_dim_based_on_win_dim(
            run_first_time, 
            window, 
            window.get_elem(self.EXPLANATION), 
            self.__EXPLANATION_DIM, 
            dynamic_width=True
        )
        
        if self.input_text_box.handle_inputs(window, run_first_time) and self.llm.model != None:
            window.input_stream.end_input_stream()
            input = window.get_elem(self.input_text_box.text_box_name).text
            self.llm.set_input_text(input)
            
            output = self.llm.get_output()
            window.get_elem(self.output_text_box.text_box_name).update_text(window.win_dim, output)
            
            glob.get_tag(self.__LOADING_BAR).display = True
            window.events()
            window.draw()
            CounterfactualGenerator.get_output(window, input, output, self.llm)
            glob.get_tag(self.__LOADING_BAR).display = False
            window.get_elem(self.__LOADING_BAR_TEXT).update_text(self.LOADING_TEXT)
        
        self.output_text_box.handle_inputs(window, run_first_time)
    
        
        self.__handel_scroll(window)
        
        
        
        
        