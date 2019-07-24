#get_columns.py
import numpy as np
import pandas as pd
import glob
import os
import sys

def save_csv (file, columns):
    # saves selected columns of file into a new csv.
    # file is a string, and columns is a list of integers.
    # returns saved dataframe and new filename

    if os.path.getsize(file) == 0: # checks if file is empty
        print ("File is empty. Skipping file")
        return pd.DataFrame(), os.path.splitext(file)[0] + "_column_restricted.csv" # returns default dataframe and default filename

    df = pd.read_csv(file, header=None) #fills dataframe with info from csv file
    column_restricted_df = df.iloc[:,columns] #selects columns

    new_name = os.path.splitext(file)[0] + "_column_restricted.csv" #modifies original filename

    column_restricted_df.to_csv(new_name, index=False) #saves csv to file of name new_name
    return column_restricted_df, new_name # returns saved dataframe and new filename


def main():
    input_length = len(sys.argv) #saves length of command line input
    if input_length <= 1:
        print ("please input a filename and/or column") #gives error message for lack of input
    else:
        regex = sys.argv[1] #saves filename regex
        file_list = glob.glob(regex) #saves list of filenames

        columns = list(map(int, sys.argv[2:input_length])) #saves list of selected columns

        i = 1 #variable for saving current position in list
        print (file_list)
        print (regex)
        for file in file_list:
            output = save_csv(file, columns) #saves new csv file and saves method output
            print ("Saved new csv file with path: " + output[1])
            print ("output {0} of {1}".format(i, len(file_list)))
            i+=1 #increases i to new index


if __name__ == "__main__":
    main()
