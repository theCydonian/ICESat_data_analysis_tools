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

def save_csv (file):
    # saves selected columns of file into a new csv.
    # file is a string, and columns is a list of integers.
    # returns saved dataframe and new filename
    df = pd.read_csv(file, header=None) #fills dataframe with info from csv file
    print("loaded dataframe")
    X = df.iloc[:,0]
    Y = df.iloc[:,1]
    Z = df.iloc[:,2]
    print("loaded xyz")

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True)

    plt.show()

    return df, file # returns saved dataframe and new filename


def main():
    input_length = len(sys.argv) #saves length of command line input
    if input_length <= 1:
        print ("please input a filename and/or column") #gives error message for lack of input
    else:
        regex = sys.argv[1] #saves filename regex
        file_list = glob.glob(regex) #saves list of filenames

        i = 1 #variable for saving current position in list
        for file in file_list:
            output = save_csv(file) #saves new csv file and saves method output
            print ("Graphed CSV with name: " + output[1])
            print ("output {0} of {1}".format(i, len(file_list)))
            i+=1 #increases i to new index


if __name__ == "__main__":
    main()
