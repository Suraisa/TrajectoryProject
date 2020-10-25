# Python Anaconda Project
# Gomes Cardoso Raphaël and Richard YUNE 


--- Project purpose ---
Project to plot flight trajectories of flights performing take off and flights performing landing around Paris.

The map is set to show the county of "Ile-de-France". The basemap shows :
- the boudaries of the municipalities in black lines
- the river flows in blue lines
- the water areas in blue surfaces
- the forest areas having more than 500 hectares in green surfaces

The take off and landing flights are selected with vertical rates and altitude thresholds


--- How to use the software ---
Ensure that you have all the required packages described in the "setup" file. 
Open the notebook file "TrajectoryProject.ipynb" and follow the instructions.



--- Folder management ---
#data folder:
Have :
- The datas of the flights that were recovered from the antenna devices in *.pkl format.
- The shapefiles associated with the basemap 


#Trajectory folder:
Contain the .py modules.
The 'ProcessManager' module manage all the other modules. It deals with:
- map : recovers the shapefile data + extract and display the basemap of the department of "ile-de-france"
- trajectories : recovers the .pkl files + extract and filter the selected data + plot the trajectories of the flights on the basemap
 


