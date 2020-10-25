import numpy as np
from pyproj import Transformer

class Projector():
    """Mother class for projector.
    It's just here to specify that all projector has their own convert static method.
    """
    @staticmethod
    def convert(lon: np.array, lat: np.array):
        """Convert longitude and latitude coordinates into another type of coordinates.
        
        Parameters:
            - lon: A numpy array of longitude coordinates 
            - lat: A numpy array of latitude coordinates

        Return:
            2 arrays into a new type of coordinates (Here it's two 0 array of same length)
        """
        return lon*0, lat*0

class Mercator(Projector):
    """Transform WGS84 into a Mercator coordinates"""
    @staticmethod
    def convert(lon, lat):
        """Convert longitude and latitude coordinates into Mercator coordinates.
        
        Parameters:
            - lon: A numpy array of longitude coordinates 
            - lat: A numpy array of latitude coordinates

        Return:
            2 arrays into a Mercator coordinates 
        """
        x = np.radians(lon)
        y = np.log(np.tan(np.radians(lat))+1/np.cos(np.radians(lat)))
        return x, y

class Lambert93(Projector):
    """Transform WGS84 into a Lambert93 coordinates"""
    @staticmethod
    def convert(lon, lat):
        """Convert longitude and latitude coordinates into Lambert93 coordinates.
        
        Parameters:
            -lon: A numpy array of longitude coordinates 
            -lat: A numpy array of latitude coordinates

        Return:
            2 arrays into a Lambert93 coordinates 
        """
        if lon.size == 0:
            return []
        if lat.size == 0:
            return []

        transformer = Transformer.from_crs(4326, 2154)

        return transformer.transform(lat,lon)
