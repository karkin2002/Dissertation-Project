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
    
    __DIM = (40, 250)
    TEXT_BOX_TITLE_FONT = "TEXT_BOX_TITLE_FONT"
    WHITE_TEXT = "WHITE_TEXT"
    TEXT_BOX_BG = "TEXT_BOX_BG"
    PG_FONT_REGULAR = "PG_FONT_REGULAR"
    
    BUTTON_PRESS_IMG = "button_press"
    BUTTON_UNPRESS_IMG = "button_unpress"
    BUTTON_WARNING = "button_warning"
    SUBMIT_UNPRESS = "submit_unpress"
    SUBMIT_PRESS = "submit_press"
    
    def __init__(self, 
                 page_elements, 
                 window: WindowUI,
                 text_box_name: str, 
                 offset: tuple[int, int], 
                 title_text: str,
                 edit: bool = True):
        
        self.edit = edit
        
        self.title_name = text_box_name + "_TITLE"
        self.text_box_name = text_box_name + "_TEXT_BOX"
        self.copy_button_name = text_box_name + "_COPY_BUTTON"
        self.paste_button_name = text_box_name + "_PASTE_BUTTON"
        self.clear_button_name = text_box_name + "_CLEAR_BUTTON"
        self.submit_button_name = text_box_name + "_SUBMIT_BUTTON"
        self.offset = offset
        self.title_text = title_text
        
        self.__setup_ui_elems(page_elements, window)
    
        
    def __setup_ui_elems(self, 
                         page_elements, 
                         window: WindowUI):
        
        page_elements.append(window.add_elem(
            self.title_name,
            Text(
                self.title_text,
                self.TEXT_BOX_TITLE_FONT,
                self.WHITE_TEXT,
                offset=self.offset,
                centered=False,
                align_top = True,
                align_left = True
            )
        ))

        page_elements.append(window.add_elem(
            self.text_box_name,
            TextBox(
                self.__DIM,
                self.TEXT_BOX_BG,
                "",
                self.PG_FONT_REGULAR,
                self.WHITE_TEXT,
                (self.offset[0], self.offset[1] + 60),
                centered=False,
                align_top = True,
                align_left = True
            )
        ))
        
        
        if self.edit:
        
            clear_button_pos =  (self.offset[0] - 110, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.clear_button_name,
                Button(
                    Image(
                        self.BUTTON_UNPRESS_IMG,
                        scale = 0.032,
                        offset = clear_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.BUTTON_WARNING,
                        scale = 0.035,
                        offset = clear_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.BUTTON_WARNING,
                        scale = 0.032,
                        offset = clear_button_pos,
                        align_right = True, 
                        align_top = True
                    )
                )
            ))

            
            
            paste_button_pos =  (self.offset[0] - 180, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.paste_button_name,
                Button(
                    Image(
                        self.BUTTON_UNPRESS_IMG,
                        scale = 0.032,
                        offset = paste_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = 0.035,
                        offset = paste_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = 0.032,
                        offset = paste_button_pos,
                        align_right = True, 
                        align_top = True
                    )
                )
            ))
            
            copy_button_pos =  (self.offset[0] - 250, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.copy_button_name,
                Button(
                    Image(
                        self.BUTTON_UNPRESS_IMG,
                        scale = 0.032,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = 0.035,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = 0.032,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True
                    )
                )
            ))
            
            submit_button_pos =  (self.offset[0] - 365, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.submit_button_name,
                Button(
                    Image(
                        self.SUBMIT_UNPRESS,
                        scale = 0.032,
                        offset = submit_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.SUBMIT_PRESS,
                        scale = 0.035,
                        offset = submit_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.SUBMIT_PRESS,
                        scale = 0.032,
                        offset = submit_button_pos,
                        align_right = True, 
                        align_top = True
                    )
                )
            ))
            
        else:
            
            copy_button_pos =  (self.offset[0] - 110, self.offset[1]+20)
            page_elements.append(window.add_elem(
                self.copy_button_name,
                Button(
                    Image(
                        self.BUTTON_UNPRESS_IMG,
                        scale = 0.032,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = 0.035,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True
                    ),
                    Image(
                        self.BUTTON_PRESS_IMG,
                        scale = 0.032,
                        offset = copy_button_pos,
                        align_right = True, 
                        align_top = True
                    )
                )
            ))
        

    def handle_inputs(self, window: WindowUI, run_first_time: bool):
        text_box_elem = window.get_elem(self.text_box_name)
        
        set_dim_based_on_win_dim(
            run_first_time, 
            window, 
            text_box_elem, 
            self.__DIM, 
            dynamic_width=True
        )
        
                    
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
        
        
        return False