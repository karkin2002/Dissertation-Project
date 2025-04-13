from scripts.ui.ui import WindowUI
from scripts.ui.ui_element import Text, TextBox, Button, Image
import pyperclip
import scripts.utility.glob as glob
glob.init()

def set_dim_based_on_win_dim(run_first_time, window, ui_element, box_dim, dynamic_width = False, dynamic_height = False):
    
    if window.resized or window.rescaled or run_first_time:
        
        if dynamic_width:
            width = (window.win_dim[0] - ((box_dim[0]*glob.scale)*2)) / glob.scale
        else:
            width = box_dim[0]
        
        if dynamic_height:
            height = (window.win_dim[1] - ((box_dim[1]*glob.scale)*2)) / glob.scale
        else:
            height = box_dim[1]
        
        if width < 0:
            width = 0
        if height < 0:
            height = 0
        
        ui_element.box_dim = (width, height)
        
        ui_element.set_surf(window.win_dim)





class TextBoxUIElem:
    
    DIM = (40, 250)
    TEXT_BOX_TITLE_FONT = "TEXT_BOX_TITLE_FONT"
    WHITE_TEXT = "WHITE_TEXT"
    TEXT_BOX_BG = "TEXT_BOX_BG"
    PG_FONT_REGULAR = "PG_FONT_REGULAR"
    TITLE_TEXT = "TITLE_TEXT"
    ICON_FONT = "ICON_FONT"
    PG_FONT_BOLD = "PG_FONT_BOLD"
    ICON_TEXT_FONT = "ICON_TEXT_FONT"
    OUTLINE_WIDTH = 5
    OUTLINE_COLOUR = "TEXT_BOX_OUTLINE"
    BOARDER_RADIUS = 20
    
    BUTTON_PRESS_IMG = "button_press"
    BUTTON_UNPRESS_IMG = "button_unpress"
    BUTTON_WARNING = "button_warning"
    SUBMIT_UNPRESS = "submit_unpress"
    SUBMIT_PRESS = "submit_press"
    
    BUTTON_IMAGE_SCALE = 0.035
    BUTTON_IMAGE_SCALE_LARGE = 0.038
    
    def __init__(self, 
                 page_elements, 
                 window: WindowUI,
                 text_box_name: str, 
                 offset: tuple[int, int], 
                 title_text: str,
                 edit: bool = True,
                 settings: bool = False,
                 background: bool = True,
                 tags: list[str] = []):
        
        self.edit = edit
        
        self.title_name = text_box_name + "_TITLE"
        self.text_box_name = text_box_name + "_TEXT_BOX"
        self.copy_button_name = text_box_name + "_COPY_BUTTON"
        self.paste_button_name = text_box_name + "_PASTE_BUTTON"
        self.clear_button_name = text_box_name + "_CLEAR_BUTTON"
        self.submit_button_name = text_box_name + "_SUBMIT_BUTTON"
        self.settings_button_name = text_box_name + "_SETTINGS_BUTTON"
        self.offset = offset
        self.title_text = title_text
        self.settings = settings
        self.background = background
        self.tags = tags
        
        self.__setup_ui_elems(page_elements, window)
    
        
    def __setup_ui_elems(self, 
                         page_elements, 
                         window: WindowUI):
        
        page_elements.append(window.add_elem(
            self.title_name,
            Text(
                self.title_text,
                self.TEXT_BOX_TITLE_FONT,
                self.TITLE_TEXT,
                offset=self.offset,
                centered=False,
                align_top = True,
                align_left = True,
                tags=self.tags,
            )
        ))
        
        
        if self.background:

            page_elements.append(window.add_elem(
                self.text_box_name,
                TextBox(
                    self.DIM,
                    "",
                    self.PG_FONT_REGULAR,
                    self.WHITE_TEXT,
                    self.TEXT_BOX_BG,
                    self.OUTLINE_WIDTH,
                    self.OUTLINE_COLOUR,
                    self.BOARDER_RADIUS,
                    (self.offset[0], self.offset[1] + 60),
                    centered=False,
                    align_top = True,
                    align_left = True,
                    tags=self.tags
                )
            ))
        
        else:
            
            page_elements.append(window.add_elem(
                self.text_box_name,
                TextBox(
                    self.DIM,
                    "",
                    self.PG_FONT_REGULAR,
                    self.WHITE_TEXT,
                    None,
                    offset = (self.offset[0], self.offset[1] + 60),
                    centered=False,
                    align_top = True,
                    align_left = True,
                    tags=self.tags
                )
            ))
        
        if self.edit:
        
            clear_button_pos =  (self.offset[0] - 110, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.clear_button_name,
                Button(
                    Image(
                        self.BUTTON_UNPRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = clear_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.BUTTON_WARNING,
                        scale = self.BUTTON_IMAGE_SCALE_LARGE,
                        offset = clear_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.BUTTON_WARNING,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = clear_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    )
                )
            ))
            
            page_elements.append(window.add_elem(
                self.clear_button_name + "ICON",
                Text(
                    "\\",
                    self.ICON_FONT,
                    self.WHITE_TEXT,
                    offset = clear_button_pos,
                    centered=True,
                    align_top = True,
                    align_right = True,
                    tags=self.tags
                )
            ))

            
            
            paste_button_pos =  (self.offset[0] - 180, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.paste_button_name,
                Button(
                    Image(
                        self.BUTTON_UNPRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = paste_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE_LARGE,
                        offset = paste_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = paste_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    )
                )
            ))
            
            page_elements.append(window.add_elem(
                self.paste_button_name + "ICON",
                Text(
                    "|",
                    self.ICON_FONT,
                    self.WHITE_TEXT,
                    offset = paste_button_pos,
                    centered=True,
                    align_top = True,
                    align_right = True,
                    tags=self.tags
                )
            ))
            
            copy_button_pos =  (self.offset[0] - 250, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.copy_button_name,
                Button(
                    Image(
                        self.BUTTON_UNPRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE_LARGE,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    )
                )
            ))
            
            page_elements.append(window.add_elem(
                self.copy_button_name + "ICON",
                Text(
                    "{",
                    self.ICON_FONT,
                    self.WHITE_TEXT,
                    offset = copy_button_pos,
                    centered=True,
                    align_top = True,
                    align_right = True,
                    tags=self.tags
                )
            ))
            
            submit_button_pos =  (self.offset[0] - 435, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.submit_button_name,
                Button(
                    Image(
                        self.SUBMIT_UNPRESS,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = submit_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.SUBMIT_PRESS,
                        scale = self.BUTTON_IMAGE_SCALE_LARGE,
                        offset = submit_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.SUBMIT_PRESS,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = submit_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    )
                )
            ))
            
            page_elements.append(window.add_elem(
                self.submit_button_name + "ICON",
                Text(
                    "SUBMIT",
                    self.ICON_TEXT_FONT,
                    self.WHITE_TEXT,
                    offset = submit_button_pos,
                    centered=True,
                    align_top = True,
                    align_right = True,
                    tags=self.tags
                )
            ))
            
        else:
            
            copy_button_pos =  (self.offset[0] - 110, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.copy_button_name,
                Button(
                    Image(
                        self.BUTTON_UNPRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE_LARGE,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = self.BUTTON_IMAGE_SCALE,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True,
                        tags=self.tags
                    )
                )
            ))
            
            page_elements.append(window.add_elem(
                self.copy_button_name + "ICON",
                Text(
                    "{",
                    self.ICON_FONT,
                    self.WHITE_TEXT,
                    offset = copy_button_pos,
                    centered=True,
                    align_top = True,
                    align_right = True,
                    tags=self.tags
                )
            ))
            
            
            if self.settings:
                settings_button_pos =  (self.offset[0] - 180, self.offset[1]+20)
                page_elements.append(window.add_elem(
                    self.settings_button_name,
                    Button(
                        Image(
                            self.BUTTON_UNPRESS_IMG,
                            scale = self.BUTTON_IMAGE_SCALE,
                            offset = settings_button_pos,
                            align_right = True, 
                            align_top = True,
                            tags=self.tags
                        ),
                        Image(
                            self.BUTTON_PRESS_IMG,
                            scale = self.BUTTON_IMAGE_SCALE_LARGE,
                            offset = settings_button_pos,
                            align_right = True, 
                            align_top = True,
                            tags=self.tags
                        ),
                        Image(
                            self.BUTTON_PRESS_IMG,
                            scale = self.BUTTON_IMAGE_SCALE,
                            offset = settings_button_pos,
                            align_right = True, 
                            align_top = True,
                            tags=self.tags
                        )
                    )
                ))
                
                page_elements.append(window.add_elem(
                    self.settings_button_name + "ICON",
                    Text(
                        "]",
                        self.ICON_FONT,
                        self.WHITE_TEXT,
                        offset = settings_button_pos,
                        centered=True,
                        align_top = True,
                        align_right = True,
                        tags=self.tags
                    )
                ))
        

    def handle_inputs(self, window: WindowUI, run_first_time: bool, custom_dim: tuple[int, int] = None):
        text_box_elem = window.get_elem(self.text_box_name)
        
        dim = self.DIM if custom_dim is None else custom_dim
        
        set_dim_based_on_win_dim(
            run_first_time, 
            window, 
            text_box_elem, 
            dim, 
            dynamic_width=True
        )
        
        if not glob.get_tag("OUTPUT_SETTINGS").display:
        
            if window.is_pressed(self.copy_button_name):
                pyperclip.copy(window.get_elem(self.text_box_name).text)
                
            elif self.edit:
                
                if window.is_pressed(self.text_box_name):
                    window.input_stream.set_input_stream(text_box_elem)
                    
                if window.is_pressed(self.clear_button_name):
                    window.get_elem(self.text_box_name).update_text(window.win_dim,  "")
                
                if window.is_pressed(self.paste_button_name):
                    window.get_elem(self.text_box_name).update_text(
                        window.win_dim, 
                        window.get_elem(self.text_box_name).text + pyperclip.paste())
                    
                return window.is_pressed(self.submit_button_name)
            
            elif self.settings:
                return window.is_pressed(self.settings_button_name)
        
        
        return False