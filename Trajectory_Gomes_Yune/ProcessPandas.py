import pandas as pd
import re
import numpy as np
from Trajectory_Gomes_Yune.FlightCollection import FlightCollection
from pathlib import PurePath
from Trajectory_Gomes_Yune.Projector import Lambert93
import os


class ProcessPandas:
    thresh_take_off_vRate = 500
    thresh_landing_vRate = -500
    thresh_min = 10000

    def __init__(self, paths):
        """Constructor :

        Parameters :
        - paths = path of the files .pkl to open 
        """
        self.datas = self.read_pickles(paths)
        self.flightCollection = FlightCollection(self.datas)

    def __iter__(self):
        yield from self.flightCollection

    def read_pickles(self, paths):
        """Read several .pkl files by concatenation

        Parameters :
        - paths = path of the files .pkl to open
        
        Return : one dataframe containing all the data 
        """
        if isinstance(paths, list):
            datas = pd.read_pickle(PurePath(paths[0]))
        
            for path in paths[1:]:
                datas = pd.concat([datas, pd.read_pickle(PurePath(path))])
        else:
            datas = pd.read_pickle(PurePath(paths))

        return datas

    def get_take_off_icao24(self):
        """Return all the datas of the flights that are performing a take off (sorted by vertical rate and altitude) """
        return [flight for flight in self.flightCollection if (flight.vertical_rate.mean() > self.thresh_take_off_vRate) & (flight.altitude.min() < self.thresh_min)]

    def get_landing_icao24(self):
        """Return all the datas of the flights that are performing a landing (sorted by vertical rate and altitude) """
        return [flight for flight in self.flightCollection if (flight.vertical_rate.mean() < self.thresh_landing_vRate) & (flight.altitude.min() < self.thresh_min)]

    def get_lon_lat(self, data):
        """Return x and y coordinates in Lambert93 reference system
        
        Parameters :
        - data : dataframe containing flight data including longitude and latitude (WGS84 system)
        
        Return converted longitude and latitude in Lambert93 """
        conv = Lambert93.convert(data.query("longitude == longitude").longitude.to_numpy(), data.query("latitude == latitude").latitude.to_numpy())
        
        if conv == []:
            return conv

        return np.vstack(conv)

    def iter_take_off_pos(self):
        """Return the position (x,y in Lambert93 system) of each flight (sorted by icao24 reference) performing a take-off """ 
        for flight in self.get_take_off_icao24():
            yield self.get_lon_lat(flight)
    
    def iter_landing_off_pos(self):
        """Return the position (x,y in Lambert93 system) of each flight (sorted by icao24 reference) performing a landing""" 
        for flight in self.get_landing_icao24():
            yield self.get_lon_lat(flight)

    def iter_flight_pos(self):
        """iter flights in flightColletion"""
        for flight in self.flightCollection:
            yield self.get_lon_lat(flight)

    def iter_tas_norm_deg(self):
        """iter tas and heading in flightColletion"""
        for flight in self.flightCollection:
            yield (flight.TAS.to_numpy(), flight.heading.to_numpy())

    def iter_ground_norm_deg(self):
        """iter groundspeed and track in flightColletion"""
        for flight in self.flightCollection:
            yield (flight.groundspeed.to_numpy(), flight.track.to_numpy())
