#plotter_test.py
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
from scipy import stats
import argparse
print("finished import")

def graph_csv (file, color_col, time_column=None, time_min=None, time_max=None):
    # saves selected columns of file into a new csv.
    # file is a string, and columns is a list of integers.
    # returns saved dataframe and new filename
    df = pd.read_csv(file, header=None) #fills dataframe with info from csv file
    df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)] # removes outliers
    if time_column is not None:
        if time_min is None or time_max is None:
            print("time minimuns and maximums need to be defined")
            return df, file
        else:
            df = df[df.iloc[:,time_column].between(time_min, time_max)]

    print("loaded dataframe")
    X = df.iloc[:,0]
    Y = df.iloc[:,1]
    Z = df.iloc[:,2]
    print("loaded xyz")

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.scatter(X,Y,Z, cmap='viridis', c=df.iloc[:,color_col], s=0.1)
    #ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True)

    plt.show()

    return df, file # returns saved dataframe and new filename


def main():
    parser = argparse.ArgumentParser(description = "Additional Options for Command Line Input")
    parser.add_argument("-f", "--file", help = "Specify Regex for Files Used", required = True, default = "")
    parser.add_argument("-c", "--color", help = "Specify Column Used for Color", required = False, default = "2")
    parser.add_argument("-n", "--timeMinimum", help = "Specify Time Minimum for Data", required = False, default = "")
    parser.add_argument("-x", "--timeMaximum", help = "Specify Time Maximum for Data", required = False, default = "")
    parser.add_argument("-t", "--timeColumn", help = "Specify Column Used for Time", required = False, default = "")
    argument = parser.parse_args()

    input_length = len(sys.argv) #saves length of command line input

    regex = argument.file #saves filename regex
    file_list = glob.glob(regex) #saves list of filenames

    i = 1 #variable for saving current position in list
    for file in file_list:
        output = None
        if argument.timeMinimum and argument.timeMinimum and argument.timeColumn:
            output = graph_csv(file, int(argument.color),
             time_column=int(argument.timeColumn), time_min=float(argument.timeMinimum),
             time_max=float(argument.timeMaximum))
        else:
            output = graph_csv(file, int(argument.color)) #saves new csv file and saves method output
        print ("Graphed CSV with name: " + output[1])
        print ("output {0} of {1}".format(i, len(file_list)))
        i+=1 #increases i to new index


if __name__ == "__main__":
    main()
