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

from pygame import Surface, SRCALPHA
from scripts.game.MapLayer import MapLayer
from scripts.utility.logger import Logger

class Map:
    
    __ADDED_NEW_MAP_LAYER_TEXT = "Added MapLayer to index '{index}' on '{map}'."
    __ERROR_REMOVING_MAP_LAYER_TEXT = "MapLayer does not exist at indexed value."
    
    
    def __init__(self, 
                 map_dim: tuple[int, int], 
                 tile_dim: tuple[int,int] = (16, 16),
                 transparent = False):

        self.__map_layer_list: list[MapLayer] = []
        self.map_dim: tuple[int, int] = map_dim
        
        self.tile_dim: int = tile_dim
        self.map_surf_dim: tuple[int, int] = (
            self.map_dim[0] * self.tile_dim[0], 
            self.map_dim[1] * self.tile_dim[1])
        
        self.map_surf: Surface = None
        
        self.transparent = transparent
        
    
    def add_map_layer(self):
        self.__map_layer_list.append(MapLayer(self.map_dim))
        
        Logger.log_info(
            self.__ADDED_NEW_MAP_LAYER_TEXT.format(
                index = len(self.__map_layer_list) - 1,
                map = self))
        
        
    def remove_map_layer(self, layer_index: int):
        if not Logger.raise_index_error(self.__map_layer_list, 
                                        layer_index,
                                        self.__ERROR_REMOVING_MAP_LAYER_TEXT,
                                        False):
            
            del self.__map_layer_list[layer_index]


    def set_map_layer(self, layer_index: int, layer: MapLayer):
        if not Logger.raise_index_error(self.__map_layer_list, 
                                layer_index,
                                self.__ERROR_REMOVING_MAP_LAYER_TEXT,
                                False):
            
            Logger.log_warning(
                Logger.__OVERWRITTEN.format(
                    data_type = MapLayer,
                    name = layer_index,
                    pre_data = self.__map_layer_list[layer_index],
                    post_data = layer
                    )
            )
            
            self.__map_layer_list[layer_index] = layer
            
    def get_map_layer(self, layer_index: int) -> MapLayer:
        
        if not Logger.raise_index_error(self.__map_layer_list, 
                                        layer_index,
                                        self.__ERROR_REMOVING_MAP_LAYER_TEXT,
                                        False):
            
            return self.__map_layer_list[layer_index]
        
    def get_map_layer_list_len(self) -> int:
        return len(self.__map_layer_list)
            
            
    def set_map_surf(self):
        if self.transparent:
            self.map_surf = Surface(self.map_surf_dim, SRCALPHA)
        else:
            self.map_surf = Surface(self.map_surf_dim)
            
        self.draw_map_layers()
                
                
    def draw_map_layers(self):
        
        for layer in self.__map_layer_list:
            for y in range(len(layer.map_array)):
                for x in range(len(layer.map_array[y])):
                    if layer.map_array[y][x] != None:
                        self.map_surf.blit(
                            layer.map_array[y][x].get_texture_surf(), 
                            (self.tile_dim[0] * x, self.tile_dim[1] * y))
        
                