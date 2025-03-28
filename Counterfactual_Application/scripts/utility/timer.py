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

import time, scripts.utility.glob as glob
glob.init()

class Timer:
    
    def __init__(self):
        """
        Initializes the Timer object.
        """
        
        self.__start_time = None
        self.__timer_length_in_sec = None

    def start(self, timer_length_in_sec: float):
        """
        Starts the timer.
        
        Args:
            timer_length_in_sec (float): The length of the timer in seconds.
        """
        
        self.__start_time = time.time()
        self.__timer_length_in_sec = timer_length_in_sec
        

    def elapsed_time(self):
        """
        Calculates the elapsed time since the timer was started.
        
        Returns:
            float: The elapsed time in seconds.
        """
        
        if self.__start_time != None:
            return time.time() - self.__start_time
        
    def is_end(self):
        """
        Check if the timer has reached its end.
        
        Returns:
            bool: True if the timer has reached its end, False otherwise.
        """
        
        if self.__start_time != None:
            return (time.time() - self.__start_time) >= self.__timer_length_in_sec
        
        return False