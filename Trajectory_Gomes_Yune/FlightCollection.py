from datetime import timedelta
from Trajectory_Gomes_Yune.Flight import Flight

class FlightCollection:
    """Class to represent a Collection of flight to separate them by a unique combination of icao24 and callsign"""

    def __init__(self, data):
        """Constructor
        
        Parameter:
            - data: It's a dataframe of flight
        """

        self.data = data
    
    def __repr__(self):
        return "Number of groups: {}".format(len(self))
    
    
    def __iter__(self):
        """It yield a group of unique combination of icao24 and callsign"""
        
        for _, group in self.data.groupby(["icao24", "callsign"]):
            yield group
                
    def __len__(self):
        return sum(1 for _ in self)
    
    def __getitem__(self, index):
        """Select an item of self.data for a icao24, a callsign or a timestamp
        
        Parameter:
            index: str for icao24 or callsign
            index: pd.Timestamp for a timestamp

        Return:
            The selected item
        """

        filters = None
        if isinstance(index, str):
            filters = (self.data.callsign == index) | (self.data.icao24 == index)
        elif isinstance(index, pd.Timestamp):
            delta = timedelta(days=1)
            filters = (index < self.data.timestamp) & (self.data.timestamp < (index + delta))
        else:
            return None

        items = FlightCollection(self.data[filters])
        
        if len(items) == 1:
            return Flight(items.data)

        return items