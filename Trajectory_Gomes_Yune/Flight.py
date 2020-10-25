class Flight:
    """Class used with FlightCollection to obtain a dataframe for a day with a unique combination of an icao24 and a callsign"""
    
    def __init__(self, data):
        """Constructor
        
        Parameter:
            - data: It's a dataframe with a unique icao24 and a unique callsign
        """
        self.data = data
    def __repr__(self):
        return (
            """Callsign: {}
icao24: {}
date :
{}\n""".format(self.callsign, self.icao24, self.data.timestamp.dt.strftime('%Y-%m-%d')))
    
    def __lt__(self, other):
        """Operator < : sorted by timestamp""" 
        return self.min("timestamp") < other.min("timestamp")

    def max(self, feature):
        """Give the max value of a feature in the self.data

        Parameter:
            - feature: it's a column name in string from the dataframe in self.data

        Return:
            The max from the selected feature
        """
        return self.data[feature].max()

    def min(self, feature):
        """Give the min value of a feature in the self.data

        Parameter:
            - feature: it's a column name in string from the dataframe in self.data

        Return:
            The min from the selected feature
        """
        return self.data[feature].min()
    
    @property
    def callsign(self):
        """Give the Callsign of this flight

        Return:
            The callsign of this flight
        """
        return self.data.callsign.iloc[0]
    
    @property
    def icao24(self):
        """Give the icao24 of this flight

        Return:
            The icao24 of this flight
        """
        return self.data.icao24.iloc[0]
    