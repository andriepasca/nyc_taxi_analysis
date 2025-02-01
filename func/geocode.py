import numpy as np
import pandas as pd
import reverse_geocoder as rg
import osmnx as ox

def reversegeocoder(location, df, lat_index, long_index):
    g = ox.graph_from_place(location, network_type='drive')
    nodes = []
    coord_ = np.zeros((len(df),2))
    for i in range(len(df)):
        coord_[i][0] = df.iloc[i,lat_index]
        coord_[i][1] = df.iloc[i,long_index]
    coord_list = [tuple(l) for l in coord_]

    df_result = pd.DataFrame()
    for i in range(len(coord_list)):
        result = pd.DataFrame(rg.search(coord_list[i]))
        node = ox.distance.get_nearest_node(g, coord_list[i], method='haversine', return_dist=False)
        nodes.append(node)
        df_result = df_result.append(result, ignore_index=True)

    df_result['projected coordinate'] = nodes
    return df_result