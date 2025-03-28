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

from pygame import Surface
from scripts.utility.logger import Logger
from scripts.game.Tile import StaticTile, DynamicTile
import numpy as np

class MapLayer:
    
    __GENERATE_NEW_MAP_TEXT = "Generated new map layer of size '{map_dim}' with tile proabilities '{tile_probability}'."
    __GENERATE_NEW_MAP_MISMATCH_LEN_TEXT = "Mismatch length between tiles & proabilities."
    
    
    def __init__(self, map_dim: tuple[int, int]):
        
        self.map_dim: tuple[int, int] = map_dim
        self.map_array: list[list[StaticTile | DynamicTile]] = None
        
    
    def generate_map_array(self, 
                           tiles: list[str], 
                           probability: list[float]):
        
        if not Logger.raise_incorrect_len(
                probability, 
                len(tiles), 
                self.__GENERATE_NEW_MAP_MISMATCH_LEN_TEXT):
            
            new_map_array = np.random.choice(a=tiles, 
                                              p=probability, 
                                              size=self.map_dim)
            
            self.map_array = [[None for _ in range(self.map_dim[1])] for _ in range(self.map_dim[0])]
            
            for y in range(len(new_map_array)):
                for x in range(len(new_map_array[y])):
                    if new_map_array[y][x] == None:
                        self.map_array[y][x] = None
                    else:
                        self.map_array[y][x] = StaticTile(new_map_array[y][x])
                
            ## --- Used for logging ---
            tile_probability: list[tuple[float, str]] = []
            
            for i in range(len(tiles)):
                tile_probability.append((probability[i], tiles[i]))
                
            tile_probability.sort(reverse=True, key=lambda x: x[0])
            
            Logger.log_info(self.__GENERATE_NEW_MAP_TEXT.format(
                map_dim = self.map_dim, 
                tile_probability = tile_probability))
            
    
        