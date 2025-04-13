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
import platform, subprocess


class MainUI:
    
    TITLE_FONT_PATH = r"static/fonts/example_font_title.ttf"
    REGULAR_FONT_PATH = r"static/fonts/example_font_regular.ttf"
    BOLD_FONT_PATH = r"static/fonts/example_font_bold.ttf"
    ICON_FONT_PATH = r"static/fonts/icon_font.ttf"
    
    WHITE = "WHITE"
    BLACK = "BLACK"
    BG_COLOUR = "BG"
    WHITE_TEXT = "WHITE_TEXT"
    BLACK_TEXT = "BLACK_TEXT"
    TITLE_TEXT = "TITLE_TEXT"
    BUTTON_TEXT_HOVER = "BUTTON_TEXT_HOVER"
    BUTTON_TEXT = "BUTTON_TEXT"
    TEXT_BOX_BG = "TEXT_BOX_BG"
    LOADING_BAR_BOX = "LOADING_BAR_BOX"
    TEXT_BOX_OUTLINE = "TEXT_BOX_OUTLINE"
    WARNING_COLOUR = "WARNING_COLOUR"
    
    TITLE_FONT = "TITLE_FONT"
    PG_FONT_REGULAR = "PG_FONT_REGULAR"
    PG_FONT_BOLD = "PG_FONT_BOLD"
    BUTTON_FONT = "BUTTON_FONT"
    BUTTON_FONT_HOVER = "BUTTON_FONT_HOVER"
    TEXT_BOX_TITLE_FONT = "TEXT_BOX_TITLE_FONT"
    ICON_FONT = "ICON_FONT"
    ICON_TEXT_FONT = "ICON_TEXT_FONT"
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
    
    UPLOAD_TEXT = "UPLOAD_TEXT"
    __UPLOAD_TEXT_OFFSET = (295, 262)
    DEFAULT_UPLOAD_TEXT = ":   None"
    LOADED_UPLOAD_TEXT = ":   \"{llm_file_path}\""
    
    __LLM_OUTPUT = "LLM_OUTPUT"
    
    __SCROLL_SPEED = 200
    
    __LOADING_BAR = "LOADING_BAR"
    __LOADING_BAR_BOX = "LOADING_BAR_BOX"
    __LOADING_BAR_BOX_OFFSET = (0, 0)
    __LOADING_BAR_BOX_DIM = (825, 200)
    __LOADING_BAR_TEXT = "LOADING_BAR_TEXT"
    __LOADING_BAR_TEXT_OFFSET = (0, 0)
    LOADING_TEXT = "Generating Counterfactuals..."
    __LOADING_TEXT_GENERATING_OUTPUT = "Generating LLM Output..."
    
    __COUNTERFACTUAL_SUBMIT_BUTTON = "COUNTERFACTUAL_SUBMIT_BUTTON"
    __COUNTERFACTUAL_BUTTON_PRESS = "counterfactual_button_press"
    __COUNTERFACTUAL_BUTTON_UNPRESS = "counterfactual_button_unpress"
    __BUTTON_IMG_SCALE = 0.035
    __BUTTON_IMG_SCALE_LARGE = 0.037
    __COUNTERFACTUAL_OUTPUT = "COUNTERFACTUAL_OUTPUT"
    __COUNTERFACTUAL_OUTPUT_EXPLANATION = __COUNTERFACTUAL_OUTPUT + "_EXPLANATION"
    __COUNTERFACTUAL_OUTPUT_SUMMARY = __COUNTERFACTUAL_OUTPUT + "_SUMMARY"
    __COUNTERFACTUAL_OUTPUT_DIM = (40, 3000)
    
    __RED_BUTTON = "red_button"
    __GREEN_BUTTON = "green_button"
    
    __DISPLAY_ALL = "DISPLAY_ALL"
    __DISPLAY_SYNONYMS = "DISPLAY_SYNONYMS"
    __DISPLAY_CORRECT_SYNONYMS = "DISPLAY_CORRECT_SYNONYMS"
    __DISPLAY_INCORRECT_SYNONYMS = "DISPLAY_INCORRECT_SYNONYMS"
    __DISPLAY_ANTONYMS = "DISPLAY_ANTONYMS"
    __DISPLAY_CORRECT_ANTONYMS = "DISPLAY_CORRECT_ANTONYMS"
    __DISPLAY_INCORRECT_ANTONYMS = "DISPLAY_INCORRECT_ANTONYMS"
    SETTING_MENU_TEXTS = {
        __DISPLAY_ALL: "Display Full Results",
        __DISPLAY_SYNONYMS: "Display Only Synonyms",
        __DISPLAY_CORRECT_SYNONYMS: "Display Only Correct Synonyms",
        __DISPLAY_INCORRECT_SYNONYMS: "Display Only Incorrect Synonyms",
        __DISPLAY_ANTONYMS: "Display Only Antonyms",
        __DISPLAY_CORRECT_ANTONYMS: "Display Only Correct Antonyms",
        __DISPLAY_INCORRECT_ANTONYMS: "Display Only Incorrect Antonyms"
    }
    __OUTPUT_SETTINGS = "OUTPUT_SETTINGS"
    
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
        glob.add_colour(self.TEXT_BOX_OUTLINE, (57, 59, 64))
        glob.add_colour(self.TITLE_TEXT, (254, 213, 102))
        glob.add_colour(self.WARNING_COLOUR, (254, 213, 102))
        
        glob.add_font(self.TITLE_FONT, self.TITLE_FONT_PATH, 60)
        glob.add_font(self.PG_FONT_REGULAR, self.REGULAR_FONT_PATH, 30)
        glob.add_font(self.PG_FONT_BOLD, self.BOLD_FONT_PATH, 30)
        glob.add_font(self.BUTTON_FONT, self.BOLD_FONT_PATH, 35)
        glob.add_font(self.BUTTON_FONT_HOVER, self.BOLD_FONT_PATH, 35)
        glob.add_font(self.TEXT_BOX_TITLE_FONT, self.TITLE_FONT_PATH, 35)
        glob.add_font(self.ICON_FONT, self.ICON_FONT_PATH, 28)
        glob.add_font(self.ICON_TEXT_FONT, self.BOLD_FONT_PATH, 26)
        
        glob.add_img_surf("button_press", pygame.image.load(r"custom/images/button_press.png"))
        glob.add_img_surf("button_unpress", pygame.image.load(r"custom/images/button_unpress.png"))
        glob.add_img_surf("button_warning", pygame.image.load(r"custom/images/button_warning.png"))
        glob.add_img_surf("submit_unpress", pygame.image.load(r"custom/images/submit_unpress.png"))
        glob.add_img_surf("submit_unpress", pygame.image.load(r"custom/images/submit_unpress.png"))
        glob.add_img_surf("submit_press", pygame.image.load(r"custom/images/submit_press.png"))
        glob.add_img_surf("counterfactual_button_press", pygame.image.load(r"custom/images/generate_counterfactual_button_press.png"))
        glob.add_img_surf("counterfactual_button_unpress", pygame.image.load(r"custom/images/generate_counterfactual_button_unpress.png"))
        glob.add_img_surf("red_button", pygame.image.load(r"custom/images/red_button.png"))
        glob.add_img_surf("green_button", pygame.image.load(r"custom/images/green_button.png"))
        
        self.page_elements = []
        self.input_text_box = None
        self.output_text_box = None
        self.counterfactual_output_text_box = None
        self.counterfactual_summary_text_box = None
        
        self.pixels_scrolled = 0
        
        self.llm = PreTrainedLLM()
        self.llm_input = None
        self.llm_output = None
        
        self.setup_title(window)
        self.setup_upload(window)
        self.__setup_user_input(window)
        self.__setup_counterfactual_output(window)
        self.__setup_settings_menu(window)
        self.__setup_loading_bar(window)
        
        self.output_format = self.__DISPLAY_ALL
        self.counterfactual_explanations = []
    
        
    def select_folder_windows():
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        folder_path = filedialog.askdirectory()
        if folder_path:
            Logger.log_info(f"Selected folder: '{folder_path}'")
        root.destroy()
        
        return folder_path
        

    def select_folder_linux():
        
        try:
            folder_path = subprocess.check_output(["zenity", "--file-selection", "--directory"], text=True).strip()
            if folder_path:
                Logger.log_info(f"Selected folder: '{folder_path}'")
            return folder_path
        except subprocess.CalledProcessError:
            Logger.log_error("Folder selection dialog closed or no folder selected.")
            return None
        
    def select_folder() -> str:
        
        if platform.system() == "Windows":
            return MainUI.select_folder_windows()

        elif platform.system() == "Linux":
            return MainUI.select_folder_linux()
        
        else:
            Logger.raise_exception("OS not supported. Please use Windows or Linux.")
            return None
    
    def setup_title(self, window: WindowUI):
        
        ## TITLE
        self.page_elements.append(window.add_elem(
            self.TITLE,
            Text(
                self.__TITLE_TEXT,
                self.TITLE_FONT,
                self.TITLE_TEXT,
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
                self.__EXPLANATION_TEXT,
                self.PG_FONT_REGULAR,
                self.WHITE_TEXT,
                None,
                offset = self.__EXPLANATION_OFFSET,
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
        
        self.input_text_box = TextBoxUIElem(
            self.page_elements, 
            window, 
            "LLM_INPUT", 
            (40, 360), 
            "LLM Input")
        
        glob.add_tag(Tag(self.__LLM_OUTPUT, "LLM output text box", True))
        
        self.output_text_box = TextBoxUIElem(
            self.page_elements, 
            window, 
            self.__LLM_OUTPUT, 
            (40, 730), 
            "LLM Output", 
            False, 
            tags = [self.__LLM_OUTPUT])
        
        
    
    def __setup_loading_bar(self, window: WindowUI):
        glob.add_tag(Tag(self.__LOADING_BAR, "Loading Bar", False))
        
        window.add_elem(
            self.__LOADING_BAR_BOX,
            Box(
                self.__LOADING_BAR_BOX_DIM,
                self.__LOADING_BAR_BOX,
                5,
                self.WARNING_COLOUR,
                20,
                offset = self.__LOADING_BAR_BOX_OFFSET,
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
        
        
    def __setup_counterfactual_output(self, window: WindowUI):
        glob.add_tag(Tag(self.__COUNTERFACTUAL_SUBMIT_BUTTON, "Button for generating counterfactual explanations", False))
        
        submit_button_pos =  (0, 1200)
        self.page_elements.append(window.add_elem(
            self.__COUNTERFACTUAL_SUBMIT_BUTTON,
            Button(
                Image(
                    self.__COUNTERFACTUAL_BUTTON_UNPRESS,
                    scale = self.__BUTTON_IMG_SCALE,
                    offset = submit_button_pos,
                    align_top = True,
                    tags=[self.__COUNTERFACTUAL_SUBMIT_BUTTON]
                ),
                Image(
                    self.__COUNTERFACTUAL_BUTTON_PRESS,
                    scale = self.__BUTTON_IMG_SCALE_LARGE,
                    offset = submit_button_pos,
                    align_top = True,
                    tags=[self.__COUNTERFACTUAL_SUBMIT_BUTTON]
                ),
                Image(
                    self.__COUNTERFACTUAL_BUTTON_PRESS,
                    scale = self.__BUTTON_IMG_SCALE,
                    offset = submit_button_pos,
                    align_top = True,
                    tags=[self.__COUNTERFACTUAL_SUBMIT_BUTTON]
                )
            )
        ))
        
        self.page_elements.append(window.add_elem(
            self.__COUNTERFACTUAL_SUBMIT_BUTTON + "ICON",
            Text(
                "GENERATE COUNTERFACTUALS",
                self.ICON_TEXT_FONT,
                self.WHITE_TEXT,
                offset = submit_button_pos,
                centered=True,
                align_top = True,
                tags=[self.__COUNTERFACTUAL_SUBMIT_BUTTON]
            )
        ))
        
        glob.add_tag(Tag(self.__COUNTERFACTUAL_OUTPUT, "The counterfactual explanation", False))
        
                
        self.counterfactual_summary_text_box = TextBoxUIElem(
            self.page_elements, 
            window, 
            self.__COUNTERFACTUAL_OUTPUT_SUMMARY, 
            (40, submit_button_pos[1] + 100), 
            "Summary",
            False,
            background=False,
            tags=[self.__COUNTERFACTUAL_OUTPUT])
        
        
        self.counterfactual_output_text_box = TextBoxUIElem(
            self.page_elements, 
            window, 
            self.__COUNTERFACTUAL_OUTPUT_EXPLANATION, 
            (40, submit_button_pos[1] + 500), 
            "Explanation",
            False,
            True,
            background=False,
            tags=[self.__COUNTERFACTUAL_OUTPUT])
        
        
    def __add_button_to_settings_menu(self, window: WindowUI, elem_name, offset, display_text):
        window.add_elem(
            elem_name,
            Button(
                Image(
                    self.__RED_BUTTON,
                    scale = self.__BUTTON_IMG_SCALE,
                    offset = offset,
                    tags=[self.__OUTPUT_SETTINGS],
                ),
                press_elem = Image(
                    self.__GREEN_BUTTON,
                    scale = self.__BUTTON_IMG_SCALE,
                    offset = offset,
                    tags=[self.__OUTPUT_SETTINGS],
                )
            )
        )
        
        window.add_elem(
            elem_name + "_TEXT",
            Text(
                display_text,
                self.PG_FONT_BOLD,
                self.WHITE_TEXT,
                offset = (offset[0] + 40, offset[1] - 20),
                centered=False,
                tags=[self.__OUTPUT_SETTINGS],
            )
        )
        
        
    def __setup_settings_menu(self, window: WindowUI):
        glob.add_tag(Tag(self.__OUTPUT_SETTINGS, "Settings for how to display the output", False))
        
        settings_box_pos = (0, 0)
        settings_box_dim = (700, 775)
        window.add_elem(
            "SETTINGS",
            Box(
                settings_box_dim,
                self.LOADING_BAR_BOX,
                5,
                self.WARNING_COLOUR,
                20,
                offset = settings_box_pos,
                tags=[self.__OUTPUT_SETTINGS],
            )
            )
            
        window.add_elem(
            "SETTINGS_TITLE",
            Text(
                "Explanation Settings",
                self.TEXT_BOX_TITLE_FONT,
                self.WHITE_TEXT,
                offset = (0, -(settings_box_dim[1] / 2 - 50)),
                tags=[self.__OUTPUT_SETTINGS],
            )
        )
        
        spacing = 90
        starting_pos = (-275, -235)
        
        item_no = 0
        for i in self.SETTING_MENU_TEXTS:
            self.__add_button_to_settings_menu(window, i, (starting_pos[0], starting_pos[1] + (spacing * item_no)), self.SETTING_MENU_TEXTS[i])
            item_no += 1
            
        window.get_elem(self.__DISPLAY_ALL).toggle()
        
        
    def __handel_settings_menu(self, window: WindowUI):
        
        toggled_button = None
        
        for i in self.SETTING_MENU_TEXTS:
            button_elem = window.get_elem(i)
            button_toggled = button_elem.toggle_state
            
            if button_toggled == False:
                if window.is_pressed(i, toggle = True):
                    toggled_button = i
                    self.output_format = i
                    break
            
        if toggled_button != None:
            for i in self.SETTING_MENU_TEXTS:
                if i != toggled_button:
                    button_elem = window.get_elem(i)
                    if button_elem.toggle_state == True:
                        button_elem.toggle()
                        
        if window.keyboard.is_pressed("back"):
            
            window.get_elem(self.counterfactual_output_text_box.text_box_name).update_text(window.win_dim, self.counterfactual_explanations[self.output_format])
            
            glob.get_tag(self.__OUTPUT_SETTINGS).display = False
                
                
                    
                

        
        
        
        
        
        
        
        
    
    def handle_inputs(self, window: WindowUI, run_first_time: bool):
    
        set_dim_based_on_win_dim(
        run_first_time, 
        window, 
        window.get_elem(self.EXPLANATION), 
        self.__EXPLANATION_DIM, 
        dynamic_width=True
        )
        
        if glob.get_tag(self.__OUTPUT_SETTINGS).display:
            self.__handel_settings_menu(window)
        
        else:
            if window.is_pressed(self.UPLOAD):
                folder_path = MainUI.select_folder()
                window.get_elem(self.UPLOAD_TEXT).update_text(window.win_dim, self.LOADED_UPLOAD_TEXT.format(llm_file_path=folder_path))
                self.llm.set_model_folder_path(folder_path)
        
        
        if self.input_text_box.handle_inputs(window, run_first_time) and self.llm.model != None:
            window.get_elem(self.__LOADING_BAR_TEXT).update_text(window.win_dim, self.__LOADING_TEXT_GENERATING_OUTPUT)
            glob.get_tag(self.__LOADING_BAR).display = True
            window.events()
            window.draw()
            
            window.input_stream.end_input_stream()
            self.llm_input = window.get_elem(self.input_text_box.text_box_name).text
            
            if self.llm_input != "":
                self.llm.set_input_text(self.llm_input)
                
                self.llm_output = self.llm.get_output()
                glob.get_tag(self.__LLM_OUTPUT).display = True
                window.get_elem(self.output_text_box.text_box_name).update_text(window.win_dim, self.llm_output)
                glob.get_tag(self.__COUNTERFACTUAL_SUBMIT_BUTTON).display = True
            
            glob.get_tag(self.__LOADING_BAR).display = False
            
            
            
        if (window.is_pressed(self.__COUNTERFACTUAL_SUBMIT_BUTTON) and 
            (self.llm_output != None  and self.llm_output != "") and
            (self.llm_input != None and self.llm_input != "")):
            
            window.get_elem(self.__LOADING_BAR_TEXT).update_text(window.win_dim, self.LOADING_TEXT)
            glob.get_tag(self.__LOADING_BAR).display = True
            window.events()
            window.draw()
            
            summary, self.counterfactual_explanations = CounterfactualGenerator.get_output(window, self.llm_input, self.llm_output, self.llm)
            
            glob.get_tag(self.__LOADING_BAR).display = False
            
            window.get_elem(self.counterfactual_summary_text_box.text_box_name).update_text(window.win_dim, summary)
            window.get_elem(self.counterfactual_output_text_box.text_box_name).update_text(window.win_dim, self.counterfactual_explanations[self.output_format])
            glob.get_tag(self.__COUNTERFACTUAL_OUTPUT).display = True
            
        self.output_text_box.handle_inputs(window, run_first_time)
        
        self.counterfactual_summary_text_box.handle_inputs(
            window, 
            run_first_time)
        
        if self.counterfactual_output_text_box.handle_inputs(window, run_first_time, self.__COUNTERFACTUAL_OUTPUT_DIM):
            glob.get_tag(self.__OUTPUT_SETTINGS).display = True
        
        self.__handel_scroll(window)
        
        
        
        
        