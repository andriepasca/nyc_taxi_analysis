import numpy as np
import pandas as pd
from collections import Counter

def tripcounter(df, origin_col_header, destination_col_header):
    trip = df[[origin_col_header, destination_col_header]]
    route = np.empty((len(trip),2), dtype=object)
    for i in range(len(trip)):
        route[i][0] = trip.iloc[i,0]
        route[i][1] = trip.iloc[i,1]
    route = route.tolist()

    count = Counter(map(tuple, route))
    recap = dict(count)
    df_recap = pd.DataFrame(recap, index=['freq'])
    df_recap = df_recap.T
    df_recap.reset_index(drop=False, inplace=True)
    return df_recap

def tripbytime(time_window,df,column_name):
    L=[0]*len(time_window)
    df[column_name] = pd.to_datetime(df[column_name])
    df.set_index(column_name, inplace=True)
    for i in range(len(time_window)):
        L[i]=df.between_time(time_window[i][0],time_window[i][1])
    return L