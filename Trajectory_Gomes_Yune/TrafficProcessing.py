import numpy as np
import pandas as pd
import Trajectory_Gomes_Yune.Projector as pj

class TrafficProcessing(object):
    def __init__(self, polar_coords : list, plane_norm_deg : list, tas_norm_deg : list, projector : pj.Projector):
        """Constructor : 

        Parameters :
        - polar_coords = list of numpy array containing longitude and latitude coordinates
        - plane_norm_deg = list of numpy array containing the groundspeed (module) and the track (angle in degrees)
        - tas_norm_deg = list of numpy array containing the true airspeed (module) and the heading (angle in degrees)
        - projector = Projector object for conversion on longitude and latitude into x and y in the wanted system (Lambert93 or Mercator)
        """

        if len(polar_coords) != len(plane_norm_deg) != len(tas_norm_deg):
            raise ValueError("{}, {} and {} should have the same length".format(polar_coords.__class__.__name__, plane_norm_deg.__class__.__name__, tas_norm_deg.__class__.__name__))
    
        self.projector = projector
        self.coords = projector.convert(polar_coords[0], polar_coords[1])
        self.plane_vect = self.vector_xy(plane_norm_deg)
        self.wind_vect = self.plane_vect - self.vector_xy(tas_norm_deg)

    def vector_xy(self, norm_deg : np.array) -> np.array:
        """Give the vector relative coordinates
        
        Parameters:
        - norm_deg = array containing the norm and the angle of the vector

        Return the coordinates x and y of the vector 
          """
        rx = norm_deg[0] * np.sin(np.radians(norm_deg[1]))
        ry = norm_deg[0] * np.cos(np.radians(norm_deg[1]))

        return np.concatenate((rx, ry), axis = 1)

    def plane_info(self) -> np.array:
         """Give the informations of the position of the plane in a given system, and the vector relative coordinates associated
          """
         return np.concatenate((self.coords, self.plane_vect), axis = 1)
        
    def wind_info(self) -> np.array:
         """Give the informations of the position of the wind in a given system, and the vector relative coordinates associated
          """
         return np.concatenate((self.coords, self.wind_vect), axis = 1)