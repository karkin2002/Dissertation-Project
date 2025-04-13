__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin, Swansea University"
__email__ = "2105361@swansea.ac.uk, karkin2002@gmail.com"

"""
--- Context
This Python program is authored by Kaya Arkin (Stu No. 2105361) as part of 
their Swansea University final year project "Exploratory Research on Explainable 
LLMs (Airbus AI Research)". The project is supervised by Mark Hall, an employee 
at the Airbus AI Research Department, and Bertie Muller, a university assigned 
supervisor. The project aims "to provide an insightful set of findings and 
recommendations on fine-turned local explanations for LLMs that can utilised as 
resource for future explainability implementations" tailored towards Airbus AI 
Research.

--- Use of External Code
The UI code in this program is based upon an engine I created outside of 
University, and therefore is not part of the project. The repo for that engine
is available at: https://github.com/karkin2002/Arctic-Engine

Any code written in their main.py or ./custom/ directory is part of the project
and is subsequently commented to reflect this.

--- Description
This file is the main file for the program.
"""

import pygame, scripts.utility.glob as glob
from scripts.utility.logger import Logger
from scripts.ui.ui import WindowUI
from custom.scripts.main_ui import MainUI

## Loading Logger and initialising.
Logger(r"logs/Counterfactual_Application")  
pygame.init()
glob.init()

## Loading window UI.
window = WindowUI(
    (1920 , 1080),
    "LLM Counterfactual Explanation",
    b_colour=MainUI.BG_COLOUR,
    framerate=9999)

main_ui = MainUI(window)

### Main Loop -----------------------------
glob.audio.setVolume(0)

run_first_time = True

run = True
while run:
    
    if window.keyboard.is_pressed("zoom_in") and glob.scale < 3:
        window.set_scale(glob.scale + 0.1)
    
    if window.keyboard.is_pressed("zoom_out") and glob.scale > 0.5:
        window.set_scale(glob.scale - 0.1)
        
    main_ui.handle_inputs(window, run_first_time)
        
    if not window.events():
        run = False
    
    window.draw()
    
    if run_first_time:
        run_first_time = False

pygame.quit()
### -----------------------------------------