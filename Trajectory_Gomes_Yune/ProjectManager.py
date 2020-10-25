import Trajectory_Gomes_Yune.Country_Maps_Route500 as cm
import Trajectory_Gomes_Yune.ProcessPandas as pp
import Trajectory_Gomes_Yune.Projector as proj
import Trajectory_Gomes_Yune.TrafficProcessing as tp
from matplotlib import pyplot as plt
from pathlib import Path
import sys

def planes_mapping():
    """
    Display taking-off, landing planes on a map
    """

    path = Path(".")
    files = list(path.glob("**/*.pkl"))
    projector = proj.Lambert93

    # We supposed that you have just one file of each
    file_commune = str(list(path.glob("**/LIMITE_ADMINISTRATIVE.shp"))[0])
    file_zone_sol = str(list(path.glob("**/ZONE_OCCUPATION_SOL.shp"))[0])
    file_zone_fleuve = str(list(path.glob("**/TRONCON_HYDROGRAPHIQUE.shp"))[0])

    print("Setup map with shapefiles.")

    maps = cm.CountryMap(file_commune, file_zone_sol, file_zone_fleuve)
    maps.setup_Maps()

    print("Get all flights infos.")

    infos = [pp.ProcessPandas(f) for f in files]

    print("Find all take off and landing flights.")

    for ind, info in enumerate(infos):
        sys.stdout.write("\r\tProcess file {} out of {}".format(ind+1, len(infos)))
        sys.stdout.flush()

        for flight in info.iter_take_off_pos():
            maps.add_plot(flight, linewidth=0.8, color="#9b44dc", alpha=1, zorder=10)

        for flight in info.iter_landing_off_pos():
            maps.add_plot(flight, linewidth=0.8, color="#f94848", alpha=1, zorder=10)

    #### Bonus 1: Have some difficulties, need work ####
    #TODO: Need to create a wind map with cluster not for each plane position 

    # for pos, ground, tas in zip(info.iter_flight_pos(), info.iter_ground_norm_deg(), info.iter_tas_norm_deg()):
    #     traffic = tp.TrafficProcessing(pos, ground, tas, projector)
    #     maps.add_arrows(traffic.wind_info())

    maps.display()
