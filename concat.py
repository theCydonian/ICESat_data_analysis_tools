#concat.py
import numpy as np
import pandas as pd
import os
import sys
import glob


def main():
    file_list = glob.glob(sys.argv[1]) # saves list of filenames from regex
    df_list = [] # initializes empty list of dataframes
    for file in file_list:
        df_list.append(pd.read_csv(file)) # adds each csv to the datframe list
    concat_df = pd.concat(df_list) # concats the dataframes
    concat_df.to_csv("concat_data.csv", index=False) # saves as new csv

if __name__ == "__main__":
    main()
