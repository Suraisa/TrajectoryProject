from matplotlib import pyplot as plt
import numpy as np
from cartopy.io.shapereader import Reader
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

class CountryMap:
    def __init__(
        self,
        path_shp_commune,
        path_shp_sol,
        path_shp_fleuve,
        proj=ccrs.LambertConformal(),
        lim_min_map=(6.085e5, 6.841e6),
        lim_max_map=(6.852e5, 6.882e6),
    ):
        """Constructor :

        Parameters :
        path_shp_* =path of the shapefiles containing the selected * information
        proj = projection definition for the axis
        lim_min_map = lower boundaries of the map Xmin and Ymin in Lambert93  
        lim_max_map =  higher boundaries of the map Xmin and Ymin in Lambert93  
        By default, the limits of the map are set to the departement of Ile-de-france
        """
    
        self.map_info_commune = self.obtain_map_info(path_shp_commune)
        self.map_info_sol = self.obtain_map_info(path_shp_sol)
        self.map_info_fleuve = self.obtain_map_info(path_shp_fleuve)
        # Definition of class variables 
        self.proj = proj
        self.lim_min_map = lim_min_map
        self.lim_max_map = lim_max_map
        self.fig = plt.figure(figsize=(20, 10))
        self.ax = plt.axes(projection=self.proj)
        # Lists of datas 
        self.commune = []
        self.foret = []
        self.eau = []
        self.fleuve = []

    def obtain_map_info(self, path):
        """ Return the records (record = (attributes, geometry)) of the shapefile

        Parameters :
        - path = path of the shapefile to read

        CountryMap(*args).obtain_map_info() ==> record :->generator"""
        self.path_shp_commune = path
        reader = Reader(path)
        records = reader.records()
        return records

    def setup_Maps(self):
        """method to obtain the filtered geometries of the delimited  areas in list form 
        CountryMap(*args).setup_Maps() ==> filtered geometries : -> geometry """
        #  Area Filter for municipality
        for geo_commune in self.map_info_commune:
            ((i, j),) = list(geo_commune.geometry.centroid.coords)
            if (
                self.lim_min_map[0] < i < self.lim_max_map[0]
                and self.lim_min_map[1] < j < self.lim_max_map[1]
            ):
                self.commune.append(geo_commune.geometry)
        # Area filter for ground items (forest and water areas) 
        for geo_sol in self.map_info_sol:
            ((i, j),) = list(geo_sol.geometry.centroid.coords)
        
            if (
                self.lim_min_map[0] < i < self.lim_max_map[0]
                and self.lim_min_map[1] < j < self.lim_max_map[1]
            ):
                if geo_sol.attributes["NATURE"] == "Forêt":
                    self.foret.append(geo_sol.geometry)
                if geo_sol.attributes["NATURE"] == "Eau":
                    self.eau.append(geo_sol.geometry)
           # Area filter for rivers
        for geo_fleuve in self.map_info_fleuve:
            ((i, j),) = list(geo_fleuve.geometry.centroid.coords)
          
            if (
                self.lim_min_map[0] < i < self.lim_max_map[0]
                and self.lim_min_map[1] < j < self.lim_max_map[1]
            ):
                self.fleuve.append(geo_fleuve.geometry)
     

    def add_plot(self, dots: np.array, **kwarg_plot):
        """ Method to add a plot

        Parameters :
        - dots : array containing the data to plot
        - kwarg_plot : parameters of the plot to be defined
        """
        self.ax.plot(*dots, **kwarg_plot)

    def display(self):
        """Display the map for a given area 
        """
        # Retrieval of filtered geometries
        commune = self.commune
        foret = self.foret
        zone_eau = self.eau
        fleuve = self.fleuve
        # Parameters of the axes to plot
        self.ax.add_geometries(
            commune, self.proj, facecolor="None", edgecolor="#000000", label="commune"
        )
        self.ax.add_geometries(
            foret,
            self.proj,
            facecolor="#14c137",
            edgecolor="#0b661d",
            alpha=0.2,
            label="zone de foret",
        )
        self.ax.add_geometries(
            zone_eau,
            self.proj,
            facecolor="#0b4fa7",
            edgecolor="#0b4fa7",
            alpha=0.2,
            label="zone d'eau",
        )
        self.ax.add_geometries(
            fleuve,
            self.proj,
            facecolor="None",
            edgecolor="#0b4fa7",
            alpha=0.7,
            label="fleuve",
        )
        # Legend adding 
        LegendElement = [
            Line2D([0], [0], color="#7347d8", lw=2,label="Avions qui décollent")
            ,
           Line2D([0], [0], color="#f94848", lw=2,label="Avions qui atterissent")
            ,
            mpatches.Patch(
                label="zone de foret",
                facecolor="#14c137",
                edgecolor="#0b661d",
                alpha=0.2,
            ),
            mpatches.Patch(
                label="zone d'eau", facecolor="#0b4fa7", edgecolor="#0b4fa7", alpha=0.2
            ),
           Line2D([0], [0],label="fleuve",lw=2, color="#0b4fa7"),
        ]
        self.ax.legend(handles=LegendElement, loc="upper right")
        # set of ax limits 
        self.ax.set_xlim(self.lim_min_map[0], self.lim_max_map[0])
        self.ax.set_ylim(self.lim_min_map[1], self.lim_max_map[1])
        self.ax.set_frame_on(False)
        plt.show()

    def add_arrow(self, line_directed, **kwarg_arrow):
        """Method to plot an arrow
        
        Parameters :
        - line_directed = x,y,dx,dy with x,y= coordinates of the base, dx,dy =coordinates of the tip"""
        self.ax.arrow(line_directed, **kwarg_arrow)

    def add_arrows(self, lines_directed, **kwarg_arrow):
        """Method to plot several arrows
        
        Parameters :
        - lines_directed = array of (x,y,dx,dy) coordinates
         with x,y= coordinates of the base, dx,dy =coordinates of the tip of each arrow to plot """
        for line in lines_directed:
            self.add_arrow(line, **kwarg_arrow)
