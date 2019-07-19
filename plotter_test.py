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

def save_csv (file, columns):
    # saves selected columns of file into a new csv.
    # file is a string, and columns is a list of integers.
    # returns saved dataframe and new filename
    df = pd.read_csv(file) #fills dataframe with info from csv file
    X = df.iloc[:,0]
    Y = df.iloc[:,1]
    Z = df.iloc[:,2]

    x1 = np.linspace(X.min(), X.max(), len(X.unique()))
    y1 = np.linspace(Y.min(), Y.max(), len(Y.unique()))
    x2, y2 = np.meshgrid(x1, y1)
    z2 = griddata((X, Y), Z, (x2, y2), method='linear')

    plotter = plt.figure().gca(projection='3d')
    plotter.plot_surface(x2, y2, z2)
    plt.show()
    
    return column_restricted_df, file # returns saved dataframe and new filename


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
