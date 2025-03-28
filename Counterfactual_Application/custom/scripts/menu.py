from scripts.ui.ui import WindowUI
from scripts.ui.ui_element import Text, Button, Image
import scripts.utility.glob as glob
from scripts.utility.glob import Tag
from scripts.utility.timer import Timer
glob.init()

    
class Menu:
    
    FPS = "fps"
    FPS_TITLE= "fps_text"
    FPS_TEXT = "FPS: {fps}"
    
    SELECTION_OFF = "{text} [OFF]"
    SELECTION_ON = "{text} [ON]"
    SELECTION_NO = "{text} [{value}]"
    GAP = 100
    
    TITLE = "title"
    SUB_TITLE = "sub_title"
    MAIN_MENU = "main_menu"
    MENU_BUTTONS = ["Continue", "New Save", "Load Save", "Settings", "Quit"]
    AUDIO_MAIN_MENU = "main_menu"
    
    OPTIONS_TITLE = "options_title"
    OPTIONS_MENU = "options"
    OPTIONS_SUB_TITLE = "options_sub_title"
    OPTIONS_BUTTONS = [("Audio", True, True), 
                       ("Music", True, True), 
                       ("UI Scale", glob.scale, False)]
    
    FPS_UPDATE_TIME_IN_SEC = 0.2
    
    music_playing = False
    
    
    def __init__(self):
        self.fps_timer = Timer()
        self.fps_timer.start(self.FPS_UPDATE_TIME_IN_SEC)
        
    
    
    def set_fps_counter(window: WindowUI):
        
        glob.add_tag(Tag(Menu.FPS, "Counter displaying the FPS", True))
        
        window.add_elem(
            Menu.FPS_TITLE,
            Text(
                Menu.FPS_TEXT.format(fps = 0),
                Menu.SUB_TITLE,
                "WHITE",
                centered = False,
                tags = [Menu.FPS],
                align_left = True,
                align_top = True
            )
        )
    
    
    
    def set_main_menu(window: WindowUI):
        
        
        glob.add_tag(Tag(Menu.MAIN_MENU, "Main menu elements.", True))


        window.add_elem(Menu.TITLE,
                        Text("UI Test Suite", "title", "WHITE", 
                            offset = (0, -330),
                            tags = [Menu.MAIN_MENU]))


        window.add_elem(Menu.SUB_TITLE,
                        Text("Kaya Arkin", "sub_title", "WHITE", 
                            offset = (0, -230),
                            tags = [Menu.MAIN_MENU]))

        offset = -80
        gap = 90
        count = 0
        for i in range(len(Menu.MENU_BUTTONS)):
            window.add_elem(
                Menu.MENU_BUTTONS[i],
                Button(
                    Text(Menu.MENU_BUTTONS[i], "menu_button_u", "WHITE", 
                            offset=(0, offset + (i * gap)), tags = [Menu.MAIN_MENU]),
                    Text(Menu.MENU_BUTTONS[i], "menu_button_h", "WHITE", 
                            offset=(0, offset + (i * gap)), tags = [Menu.MAIN_MENU]),
                    Text(Menu.MENU_BUTTONS[i], "menu_button_p", "WHITE", 
                            offset=(0, offset + (i * gap)), tags = [Menu.MAIN_MENU]),
                    ("ui", "button_3"),
                    ("ui", "button_1")))
            
        glob.audio.play(Menu.AUDIO_MAIN_MENU, "music", 99)
        Menu.music_playing = True
        
    
    
    
    def add_selection(window: WindowUI, elem_name: str, text: str, y_offset: int, default_state: bool = False):
        
        offset = (0, y_offset)
        
        window.add_elem(
            elem_name,
            Button(
                Text(Menu.SELECTION_OFF.format(text = text), 
                     "menu_button_u", 
                     "WHITE", 
                     offset = offset,
                     tags = [Menu.OPTIONS_MENU]),
                
                None,
                Text(Menu.SELECTION_ON.format(text = text), 
                     "menu_button_u", 
                     "WHITE", 
                     offset = offset,
                     tags = [Menu.OPTIONS_MENU]),
                defualt_toggle_state = default_state
            ))
        
        
    def add_no_selection(window: WindowUI, elem_name: str, text: str, y_offset: int, value: float, tags: list[str] = [], **align_args: dict[str, bool]):
        
        offset = (0, y_offset)
        
        window.add_elem(
            f"{elem_name}_text",
            Text(Menu.SELECTION_NO.format(text = text, value = value), "menu_button_u", "WHITE", 
                 offset = (0, y_offset),
                 centered=True, 
                 tags = tags,
                 **align_args)
        )
        
        text_width = window.get_elem(f"{elem_name}_text").dim[0] / 2
        button_gap = 30
            
        up_text = Text(">", 
            "menu_button_u", 
            "WHITE", 
            offset = (text_width + button_gap, y_offset),
            tags = tags,
            **align_args)
        
        h_up_text = Text(">", 
            "menu_button_h", 
            "WHITE", 
            offset = (text_width + button_gap, y_offset),
            tags = tags,
            **align_args)
        
        down_text = Text("<", 
            "menu_button_u", 
            "WHITE", 
            offset = (-text_width - button_gap, y_offset),
            tags = tags,
            **align_args)
        
        h_down_text = Text("<", 
            "menu_button_h", 
            "WHITE", 
            offset = (-text_width - button_gap, y_offset),
            tags = tags,
            **align_args)
        
        window.add_elem(
            f"{elem_name}_up", 
            Button(up_text, h_up_text, up_text))
        
        window.add_elem(
            f"{elem_name}_down", 
            Button(down_text, h_down_text, down_text))
    
            
            
    def set_options_menu(window: WindowUI):
        
        glob.add_tag(Tag(Menu.OPTIONS_MENU, "Options menu elements.", False))
        
        window.add_elem(
            Menu.OPTIONS_TITLE,
            Text("설정", "title", "WHITE", 
            offset = (0, -330),
            tags = [Menu.OPTIONS_MENU]))
        
        
        window.add_elem(Menu.OPTIONS_SUB_TITLE,
            Text("Settings", "sub_title", "WHITE", 
            offset = (0, -230),
            tags = [Menu.OPTIONS_MENU]))
        
        ### ----------- Settings --------------
        
        for i in range(len(Menu.OPTIONS_BUTTONS)):
            
            if Menu.OPTIONS_BUTTONS[i][2]:
                Menu.add_selection(
                    window, 
                    Menu.OPTIONS_BUTTONS[i][0], 
                    Menu.OPTIONS_BUTTONS[i][0],
                    i * Menu.GAP, 
                    Menu.OPTIONS_BUTTONS[i][1])
            else:
                Menu.add_no_selection(
                    window,
                    Menu.OPTIONS_BUTTONS[i][0], 
                    Menu.OPTIONS_BUTTONS[i][0],
                    i * Menu.GAP, 
                    Menu.OPTIONS_BUTTONS[i][1],
                    tags = [Menu.OPTIONS_MENU])
                
            back_offset = (18, -70)
                
            window.add_elem(
                "back", 
                Button(
                    Text("Back", "menu_button_u", "WHITE", offset=back_offset, centered=False, tags = [Menu.OPTIONS_MENU], align_left = True, align_bottom = True),
                    Text("Back", "menu_button_h", "WHITE", offset=back_offset, centered=False, tags = [Menu.OPTIONS_MENU], align_left = True, align_bottom = True),
                    Text("Back", "menu_button_p", "WHITE", offset=back_offset, centered=False, tags = [Menu.OPTIONS_MENU], align_left = True, align_bottom = True),
                    ("ui", "button_3"),
                    ("ui", "button_1")
                ))
        
        ### -----------------------------------
    
    def handle_menus(self, window: WindowUI, run: bool):
        
        if glob.get_tag(Menu.FPS).display:
            
            if self.fps_timer.is_end():
                window.update_text(
                    Menu.FPS_TITLE, 
                    Menu.FPS_TEXT.format(fps = int(window.get_fps())))

                self.fps_timer.start(Menu.FPS_UPDATE_TIME_IN_SEC)
        
        
        if glob.get_tag(Menu.MAIN_MENU).display:
            for button_name in Menu.MENU_BUTTONS:
                
                if window.is_pressed(button_name):
                
                    if button_name == "Continue":
                        glob.audio.pause(Menu.AUDIO_MAIN_MENU, "music")
                        glob.get_tag(Menu.MAIN_MENU).display = False
                        
                    elif button_name == "Settings":
                        glob.get_tag(Menu.MAIN_MENU).display = False
                        glob.get_tag(Menu.OPTIONS_MENU).display = True
                    
                    elif button_name == "Quit":
                        run = False
        
        elif glob.get_tag(Menu.OPTIONS_MENU).display:
            
            for i in Menu.OPTIONS_BUTTONS:
                button_name = i[0]
                
                if i[2]:
                    
                    if button_name == "Audio":
                        if window.is_pressed(button_name, toggle=True):
                            if glob.audio.volume <= 0:
                                glob.audio.setVolume(50)
                        else:
                            if glob.audio.volume > 0:
                                glob.audio.setVolume(0)
                    
                    elif button_name == "Music":
                        if window.is_pressed(button_name, toggle=True):
                            if not Menu.music_playing:
                                glob.audio.unpause(Menu.AUDIO_MAIN_MENU, "music")
                                Menu.music_playing = True
                        else:
                            if Menu.music_playing:
                                glob.audio.pause(Menu.AUDIO_MAIN_MENU, "music")
                                Menu.music_playing = False
                                
                    else:
                        window.is_pressed(button_name, toggle=True)
                        
                else:
                    if window.is_pressed(button_name + "_up"):
                        if button_name == "UI Scale":
                            window.set_scale(glob.scale + 0.1)
                            window.update_text(
                                button_name + "_text", 
                                Menu.SELECTION_NO.format(text=button_name, value = round(glob.scale, 1)))
                    
                    elif window.is_pressed(button_name + "_down"):
                        if button_name == "UI Scale" and glob.scale > 0.5:
                            window.set_scale(glob.scale - 0.1)
                            window.update_text(
                                button_name + "_text", 
                                Menu.SELECTION_NO.format(text=button_name, value = round(glob.scale, 1)))
                            
            if window.is_pressed("back") or window.keyboard.is_pressed("back", hold=False):
                glob.get_tag(Menu.MAIN_MENU).display = True
                glob.get_tag(Menu.OPTIONS_MENU).display = False
                
        return run