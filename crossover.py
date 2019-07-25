import numpy as np
import pandas as pd
import glob
import os
import sys
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy.interpolate import griddata
import statistics
import geopandas
import shapely

def cx(lat1, lon1, alt1, lat2, lon2, alt2, thresh):
    # Finds distance between two points, if they are within
    # threshold then return the distance, otherwise return -1
    # Assumes these are different tracks
    dist = (lat1*lat1 + lat2*lat2)**0.5
    if ((lat1*lat1 + lat2*lat2)**0.5) < thresh:
        return alt2-alt1
    return 0

def slope(file):
    lat = file.iloc[:,12]
    lon = file.iloc[:,13]
    return (lat[1]-lat[0])/(lon[1]-lon[0])

def main():
    file_list = sys.argv[1: len(sys.argv)-1] #graphs = sys.argv[len(sys.argv)-1]
    df_list = []
    for file in file_list:
        try:
            df_list.append( pd.read_csv( str( file) ) )
        except:
            continue

    deltaCX = []
    slopes = list( set( [ int( slope(df)*10) for df in df_list ] ))
    for file in df_list:
        for file2 in df_list:
            lat1 = list(file.iloc[:,12])
            lon1 = list(file.iloc[:,13])
            alt1 = list(file.iloc[:,14])

            alt2 = list(file2.iloc[:,14])
            lat2 = list(file2.iloc[:,12])
            lon2 = list(file2.iloc[:,13])
            temp = [lat1, lon1, alt1, alt2, lon2, lat2]
            temp2 = [ len(x) for x in temp]
            f = min(temp2)
            for i in range( f ):
                deltaCX.append( cx(lat1[i], lon1[i], alt1[i], lat2[i], lon2[i], alt2[i], 100 ))

    deltaCX = [d for d in deltaCX if d != 0]
    print(statistics.mean(deltaCX))
    plt.hist(deltaCX, density=True, rwidth=0.01)
    plt.show()
    plt.savefig('cxHist.png')

    plt.plot()

if __name__ == "__main__":
    main()
