#time_plotter.py
import numpy as np
import pandas as pd
import glob
import os
import sys
import matplotlib.pyplot as plt

def get_data(file, column):
    df = pd.read_csv(file, header=None)
    return df.groupby(column).mean()

def save_plot(df, file):
    plt.plot(range(len(df.iloc[:,0])), df.iloc[:,0], linewidth=2.0)
    plt.savefig(os.path.splitext(file)[0] + ".png")

def main():
    input_length = len(sys.argv) #saves length of command line input
    if input_length <= 2:
        print ("please input filename and column to divide with") #gives error message for lack of input
    else:
        regex = sys.argv[1] #saves filename regex
        file_list = glob.glob(regex) #saves list of filenames

        i = 1 #variable for saving current position in list
        column = int(sys.argv[2])
        for file in file_list:
            output = get_data(file, column)
            save_plot(output, file)


if __name__ == "__main__":
    main()
