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


from pygame import mixer
from scripts.utility.logger import Logger
from scripts.utility.basic import get_filename


MAX_NO_CHANNELS = "Max no of channels reached: '{no_channels}'"
NEW_CHANNEL_ADDED = "Added new channel. No of channels: '{no_channels}'"


## Sets volume of audio class
def setAudioVolume(audio, value):
    audio.set_volume(value/100)        


## Sets num of audio channels
def setNumChannels(value: int):

    """Sets number of audio channels (how many sounds you caan play at once).
    """

    mixer.set_num_channels(value)

## Gets the num of audio channels
def getNumChannels() -> int:

    """Returns num of audio channels.

    Returns:
        int: num of audio channels
    """

    return mixer.get_num_channels()

## Adds a new channel
def addChannel():

    """Adds a new audio channel.
    """

    setNumChannels(getNumChannels()+1)

## finds an empty channel, creates new if no empty
def findChannel(max_channels: int) -> mixer.Channel:

    """Finds a channel with no audio playing, otherwise creates a new one,
    otherwise return None.

    Returns:
        Channel: empty channel
    """

    audioChannel = mixer.find_channel()
    
    if audioChannel != None:
        return audioChannel
    
    else:
        if getNumChannels() < max_channels:
            addChannel()
            Logger.log_info(
                NEW_CHANNEL_ADDED.format(no_channels=getNumChannels()))
            return mixer.Channel(getNumChannels()-1)

        else:
            Logger.log_warning(
                MAX_NO_CHANNELS.format(no_channels=max_channels))




## Audio
class Audio:

    """Class for individual audio
    """

    def __init__(self, name: str, path: str, volume: float = 50):
        self.__name = name
        self.setVolume(volume)

        self.audio = mixer.Sound(path) 

    def getName(self):
        return self.__name

    def getVolume(self):
        return self.__volume

    def setVolume(self, value):
        self.__volume = value

    def getAudio(self):
        return self.audio

    def play(self, max_channels, loops = 0):
        channel = findChannel(max_channels)
        if channel != None:
            channel.play(self.audio, loops)




## Audio Category
class AudioCategory:
    AUDIO_ERROR = "The audio '{audio_name}' doesn't exist."
    AUDIO_ADD = "Audio '{audio_name}' added as '{audio}'"
    
    def __init__(self, name, volume, channel = False):
        self.name = name
        self.volume = volume
        self.mute = False

        self.audio_dict: dict[str, Audio] = {}
    

    ## Returns the name of the audio category
    def getName(self) -> str:

        """Returns the name of the audio category.

        Returns:
            str: audio category name
        """

        return self.name
    
    ## Returns the volume of an audio
    def getVolume(self) -> float:

        """Returns volume of the audio category

        Returns:
            float: volume
        """

        return self.volume
    
    ## checks if an audio is in the audio_dict
    def isAudio(self, name: str) -> bool:
        """Checks if an audio exists in the audio dict

        Returns:
            bool: True if audio exists, False otherwise
        """
        
        if not Logger.raise_key_error(self.audio_dict, 
                                      name, 
                                      self.AUDIO_ERROR.format(
                                          audio_name = name)):
            return True
        
        return False
    

    ## returns a audio class
    def __getAudio(self, name: str) -> Audio:

        """Returns audio from audio dict

        Returns:
            Audio: audio
        """

        return self.audio_dict[name]

    # Sets the volume of the category
    def setCatVolume(self, overall_volume: float, value: float):

        """Sets the category volume
        """
        self.volume = value
        for each_audio in self.audio_dict:
            self.setAudioVolume(each_audio, overall_volume, value)

    ## Sets the volume of an audio
    def setAudioVolume(self, name: str, overall_volume: float, value: float = None):
        
        """Sets the volume of an audio
        """
        
        if self.isAudio(name):
            audio = self.__getAudio(name)
            if value != None:
                audio.setVolume(value)

                # (overall*(category/100))*(audio/100)
                volume_value = (overall_volume * (self.volume/100)) * (audio.getVolume()/100)
                setAudioVolume(audio.getAudio(), volume_value)

    ## Returns the volume of an audio
    def getAudioVolume(self, name: str) -> int:
        """Returns the volume of an audio

        Returns:
            int: volume
        """        
        
        return self.__getAudio(name).getVolume()


    ## Adds audio to the audio_dict and sets its volume, doesn't play the audio
    def addAudio(self, name: str, path: str, overall_volume: float, volume: float = 50):

        """Adds audio to audio dict, sets its volume (doesn't play the audio)
        """

        if name == None:
            name = get_filename(path, False)
        self.audio_dict[name] = Audio(name, path, volume)
        self.setAudioVolume(name, overall_volume, volume)
        
        Logger.log_info(self.AUDIO_ADD.format(
            audio_name = name, 
            audio=self.audio_dict[name]))

    ## Plays audio
    def playAudio(self, name: str, max_channels: int, loops: int = 0):

        """Plays audio
        """

        self.__getAudio(name).play(max_channels, loops)

    ## Finds which channel an audio is playing in
    def __findChannelByAudio(self, name: str) -> mixer.Channel:

        """Returns a channel which an audio is playing in

        Returns:
            Channel: channel with audio playing
        """
        
        audio = self.__getAudio(name).audio
        for eachChannel in range(getNumChannels()):
            if mixer.Channel(eachChannel).get_sound() == audio:
                return eachChannel

    ## Pauses an audio
    def pauseAudio(self, name: str):
        """Pauses an audio
        """

        mixer.Channel(self.__findChannelByAudio(name)).pause()

    ## Unpauses an audio
    def unpauseAudio(self, name: str):
        """Unpauses an audio
        """

        mixer.Channel(self.__findChannelByAudio(name)).unpause()

    ## Queues an audio after another audio on a channel
    def queueAudio(self, audio_name: str, audio_queue_name: str):
        """Queues an audio after another audio on a specific channel
        """

        if self.isAudio(audio_name) and self.isAudio(audio_queue_name):
            channel = self.__findChannelByAudio(audio_name)
            mixer.Channel(channel).queue(self.__getAudio(audio_queue_name).getAudio())





## Class used for all audio on the UI
class AudioUI:

    """Handles all UI audio
    """
    
    CAT_ERROR = "Audio categoary '{cat_name}' doesn't exist"
    CAT_ADD = "Audio categoary '{cat_name}' created."
    CAT_EXISTS = "Audio categoary '{cat_name}' already exists."

    def __init__(self, 
            volume: float, 
            max_channels: int = 16, 
            frequency: int = 44100, 
            size: int = -16, 
            channels: int = 2, 
            buffer: int = 512, 
            device_name: str = None):
        
        self.volume = volume

        self.cat_dict = {}

        mixer.pre_init(frequency, size, channels, buffer, device_name) # Initialising the mixer
        mixer.init()

        self.max_channels = max_channels

        if max_channels < getNumChannels():
            setNumChannels(max_channels)

    ## Sets the overall volume for the application
    def setVolume(self, value: int):
        """Sets the overall volume for the application
        """        

        if self.volume != value:
            self.volume = value

            for cat_name in self.cat_dict:
                self.setCatVolume(cat_name, self.getCatVolume(cat_name))

    ## Returns the overall volume for the application
    def getVolume(self):
        """Returns the overall volume for the application

        Returns:
            float: volume
        """

        return self.volume 
        
    ## Returns whether the category exists
    def __isCat(self, cat_name: str):
        
        if not Logger.raise_key_error(self.cat_dict, 
                                      cat_name,
                                      self.CAT_ERROR.format(cat_name = cat_name)):
            return True
        
        return False

    ## Retruns the audio cat object
    def __getAudioCat(self, cat_name) -> AudioCategory:
        if self.__isCat(cat_name):
            return self.cat_dict[cat_name]

    ## Adds a new Audio Cat to a dict
    def addCat(self, cat_name: str, volume: float = 50):

        """Adds a new category
        """

        if not cat_name in self.cat_dict:
            self.cat_dict[cat_name] = AudioCategory(cat_name, volume)
            Logger.log_info(self.CAT_ADD.format(cat_name = cat_name))

        else:
            Logger.log_info(self.CAT_EXISTS.format(cat_name = cat_name))

    ## Adds an audio to an audioCat
    def addAudio(self, cat_name: str, path: str, audio_name: str = None , volume: float = 50):

        """Adds a new audio to an category
        """

        self.__getAudioCat(cat_name).addAudio(audio_name, path, self.volume, volume)
    
    ## Sets the volume of the audioCat
    def setCatVolume(self, cat_name: str, value: float):

        """Sets the category volume
        """

        self.__getAudioCat(cat_name).setCatVolume(self.volume, value)


    ## Returns the volume of the category
    def getCatVolume(self, cat_name: str) -> int:
        """Returns a categories volume

        Returns:
            int: volume
        """

        return self.__getAudioCat(cat_name).getVolume()

    ## Sets the audio in the audioCat
    def setAudioVolume(self, cat_name: str, audio_name: str, value: float):

        """Sets an audio's volume
        """

        self.__getAudioCat(cat_name).setAudioVolume(audio_name, self.volume, value)

    ## Returns the volume of the category
    def getAudioVolume(self, cat_name: str, audio_name: str) -> int:
        """Returns an audios volume

        Returns:
            int: volume
        """

        return self.__getAudioCat(cat_name).getAudioVolume(audio_name)

    ## Plays an audio
    def play(self, cat_name: str, audio_name: str, loops: int = 0):

        """Plays an audio
        """

        if self.__getAudioCat(cat_name).isAudio(audio_name):
            self.__getAudioCat(cat_name).playAudio(audio_name, self.max_channels, loops)
            #Logger.log_info(f"Playing '{audio_name}' from '{cat_name}' with {loops} loops.")

    ## Pauses the audio
    def pause(self, cat_name: str, audio_name: str):

        """Pauses an audio
        """

        if self.__getAudioCat(cat_name).isAudio(audio_name):
            self.__getAudioCat(cat_name).pauseAudio(audio_name)

    ## Unpauses the audio
    def unpause(self, cat_name: str, audio_name: str):

        """Unpauses an audio
        """

        if self.__getAudioCat(cat_name).isAudio(audio_name):
            self.__getAudioCat(cat_name).unpauseAudio(audio_name)

    ## Queue an audio
    def queue(self, cat_name: str, audio_name: str, audio_queue_name: str):

        """Queues an audio
        """

        self.__getAudioCat(cat_name).queueAudio(audio_name, audio_queue_name)