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

def graph_csv (file, color_col, x_col, y_col, z_col, time_column=None, time_min=None, time_max=None):
    # plots file and saves as csv.
    # file is a string, and columns is a list of integers.
    # returns initial dataframe and new filename
    df = pd.read_csv(file, header=None) #fills dataframe with info from csv file
    df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)] # removes outliers

    # selects specified time frame
    if time_column is not None:
        if time_min is None or time_max is None: # checks if only the time column is specified
            print("time minimuns and maximums need to be defined")
            return df, file
        else:
            df = df[df.iloc[:,time_column].between(time_min, time_max)] # saves selected rows into dataframe

    print("loaded dataframe")
    X = df.iloc[:,x_col] # loads x column as series
    Y = df.iloc[:,y_col] # loads y column as series
    Z = df.iloc[:,z_col] # loads z column as series
    print("loaded xyz")

    fig = plt.figure() # initializes empty figure
    ax = fig.gca(projection='3d') # specifies 3d space

    ax.scatter(X,Y,Z, cmap='viridis', c=df.iloc[:,color_col], s=0.1) # creates scatterplot

    plt.savefig(os.path.splitext(file)[0] + ".png") # saves graph to png

    return df, file # returns saved dataframe and new filename


def main():
    parser = argparse.ArgumentParser(description = "Additional Options for Command Line Input") # initializes parser
    parser.add_argument("-f", "--file", help = "Specifies Regex for Files Used", required = True, default = "") # file arg
    parser.add_argument("-n", "--timeMin", help = "Specifies Min Time for Data", required = False, default = "") # min time arg
    parser.add_argument("-x", "--timeMax", help = "Specifies Max Time for Data", required = False, default = "") # max time arg
    argument = parser.parse_args()

    input_length = len(sys.argv) #saves length of command line input

    regex = argument.file #saves filename regex
    file_list = glob.glob(regex) #saves list of filenames

    properties = open("plotter.properties", "r") # opens properties file
    Xi = None # initializes X column
    Yi = None # initializes Y column
    Zi = None # initializes Z column
    TIMEi = None # initializes time column
    COLORi = None # initializes color column

    # sets values of properties defined variables
    for line in properties:
        if "X=" in line:
            Xi = int(line.split('=')[1]) # sets X column index
        elif "Y=" in line:
            Yi = int(line.split('=')[1]) # sets Y column index
        elif "Z=" in line:
            Zi = int(line.split('=')[1]) # sets Z column index
        elif "TIME=" in line:
            if not len(line.split('=')[1]) <= 1:
                TIMEi = int(line.split('=')[1]) # sets TIME column index || accepts empty property
        elif "COLOR=" in line:
            COLORi = int(line.split('=')[1]) # sets COLOR colum index

    i = 1 #variable for saving current position in list
    for file in file_list: # iterates over all selected files
        output = None # initializes output
        if argument.timeMinimum and argument.timeMinimum: # checks if time arguments are not specified
            output = graph_csv(file, COLORi, Xi, Yi, Zi,
             time_column=TIMEi, time_min=float(argument.timeMinimum),
             time_max=float(argument.timeMaximum)) # saves plot
        else:
            output = graph_csv(file, COLORi, Xi, Yi, Zi) #saves plot
        print ("Plotted CSV with name: " + output[1])
        print ("output {0} of {1}".format(i, len(file_list)))
        i+=1 #increases i to new index


if __name__ == "__main__":
    main()
