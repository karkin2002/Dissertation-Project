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

from pygame import Surface, transform
from scripts.game.Map import Map
from scripts.utility.logger import Logger
from scripts.game.Tile import StaticTile, DynamicTile
from scripts.game.Camera import Camera

class ArcticEngine:
    
    __TUPLE_NOT_IN_RANGE = "{topic} not in range '{value}'. Ensure values are >= 1."
    __GAME_SURF_DIM = "Specified game surface dimensions"
    __INVALID_MAP_NAME_TEXT = "Map does not exist."
    
    DEFAULT_CAMERA_NAME = "default_camera"
    __CAMERA_NAME_NOT_EXIST = "Camera name does not exist, returning default camera."
    __ADDED_CAMERA = "Camera '{name}' added as '{data}'."
    
    def __init__(self):
        
        self.unscaled_game_surf: Surface = None
        self.unscaled_game_surf_dim: tuple[int, int] = None
        self.game_surf: Surface = None
        self.game_surf_dim: tuple[int, int] = None
        self.game_surf_pos: tuple[int, int] = (0, 0)
        
        self.map_dict: dict[str, Map] = {}
        
        self.__camera_dict: dict[str, Camera] = {
            self.DEFAULT_CAMERA_NAME: Camera()
        }
            
    def __set_unscaled_game_surf(self, surf_resized: bool, surf_dim: tuple[int, int], camera: Camera):
        
        if self.unscaled_game_surf == None or surf_resized or camera.camera_scale_changed:
            
            if all(i >= 1 for i in surf_dim):
                
                self.unscaled_game_surf_dim = (
                    (surf_dim[0] / camera.scale)+1, 
                    (surf_dim[1] / camera.scale)+1)
                
                self.unscaled_game_surf = Surface(self.unscaled_game_surf_dim)
                
                self.x_centered = self.unscaled_game_surf.get_width() % 2 == 0
                self.y_centered = self.unscaled_game_surf.get_height() % 2 == 0
            
            else:
                Logger.log_error(
                    ArcticEngine.__TUPLE_NOT_IN_RANGE.format(
                        topic = ArcticEngine.__GAME_SURF_DIM, value = surf_dim))
    
        
    def __set_game_surf_pos(self, camera: Camera) -> tuple[int, int]:
        
        x = -(camera.scale)
        if not self.x_centered:
            x += camera.scale / 2
            
        y = -(camera.scale )
        if not self.y_centered: 
            y += camera.scale / 2
            
        self.game_surf_pos = (round(x), round(y))
        
    
    def __set_scaled_game_surf(self, surf_resized: bool, surf_dim: tuple[int, int], camera: Camera):

        self.game_surf = transform.scale(self.unscaled_game_surf, (
            round(self.unscaled_game_surf_dim[0] * camera.scale),
            round(self.unscaled_game_surf_dim[1] * camera.scale)))
        
        self.game_surf_dim = surf_dim
        
        self.__set_game_surf_pos(camera)
                
                
    def __draw_map(self, map_obj: Map, camera: Camera):
        self.unscaled_game_surf.fill((0,0,0))
        
        ## Drawing the map onto the game window
        self.unscaled_game_surf.blit(map_obj.map_surf, (
            (self.unscaled_game_surf_dim[0] / 2) + round(camera.pos[0]),
            (self.unscaled_game_surf_dim[1] / 2) + round(camera.pos[1]),
        ))
        

    def set_game_surf(self, 
                      surf_resized: bool, 
                      surf_dim: tuple[int, int], 
                      map_obj: Map,
                      camera: Camera) -> Surface:
        
        ## Setting the game window
        self.__set_unscaled_game_surf(surf_resized, surf_dim, camera)
        
        ## Drawing the map
        self.__draw_map(map_obj, camera)
        
        ## Scaleding the game window to match the size of the surface being drawn on
        self.__set_scaled_game_surf(surf_resized, surf_dim, camera)
        
        camera.camera_scale_changed = False
        camera.camera_pos_changed = False
        
        
    def add_map(self, map_name: str, new_map: Map):
        
        if map_name in self.map_dict:
            Logger.log_info(Logger.__OVERWRITTEN.format(
                data_type = type(new_map),
                name = map_name,
                pre_data = self.map_dict[map_name],
                post_data = new_map
            ))
            
        self.map_dict[map_name] = new_map
        
    def get_map(self, map_name: str) -> Map:
        
        if not Logger.raise_key_error(
            self.map_dict,
            map_name,
            self.__INVALID_MAP_NAME_TEXT,
            False):
            
            return self.map_dict[map_name]
        
        return None
        
        
    def get_camera(self, camera_name: str = DEFAULT_CAMERA_NAME) -> Camera:
        
        if not Logger.raise_key_error(
            self.__camera_dict,
            camera_name,
            self.__CAMERA_NAME_NOT_EXIST,
            False):
            
            return self.__camera_dict[camera_name]
        
        return self.__camera_dict[self.DEFAULT_CAMERA_NAME]
            
            
    def add_camera(self, camera_name: str, camera: Camera) -> bool:
        
        if camera_name in self.__camera_dict:
            
            Logger.warn_overwritten(
                camera_name,
                self.__camera_dict[camera_name],
                camera
            )
            
        self.__camera_dict[camera_name] = camera
        
        Logger.log_info(self.__ADDED_CAMERA.format(
            name = camera_name,
            data = camera))