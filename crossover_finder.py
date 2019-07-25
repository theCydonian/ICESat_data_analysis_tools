#crossover_finder.py
import numpy as np
import pandas as pd
import scipy.stats as stats
import glob
import os
import sys

def solve(line_list, box):
    # input: [slope, intersect, other_stuff]
    # output: [ [], [], [], [] ]

    # Group slopes, compare lines within each group
    # box is list of top bottom left right lat/lon lines
    # 0 is left, 1 is right, 2 is top, 3 is bottom

    intersects = [] # initializes output array

    for i in range(len(line_list)):
        for j in range(len(line_list)):
            # if lines are different and have opposing slopes
            if i != j and line_list[i][0]*line_list[j][0] < 0:  #assuming slope is index 0
                intersects.append(get_intersect(line_list[i], line_list[j]))

    for i in intersects:
        if i[0] > box[0] or i[1] > box[2] or i[0] < box[3] or i[1] < box[1]: #checks if point is out of range
            intersects.remove(i)

    return intersects

def get_intersect(line1, line2):
    # slope/intercept form => [slope, intercept]
    x = (line2[1]-line1[1]) / (line1[0]-line2[0])
    y = line1[0]*x + line2[1]
    return (x,y)

def get_cx_altdist(xover_list):
    # [ [   cx point    ] , [ [xyz], [xyz] ]  , [ ]   ]
    stats =[]
    for cx in xover_list:
        alt = [] # initializes array of altitudes
        if cx is not None and len(cx)>0:
            for point in cx:
                alt.append( point[2] ) # extracts each point by crossover
        if len(alt) > 0:
            stats.append(alt) # adds list of points at each crossover
    return stats

def get_error(xover_list):
    print(xover_list)
    alt = get_cx_altdist(xover_list) # extracts altitude
    print(alt)
    df = pd.DataFrame(columns=['Number of Points', 'Range',
     'Standard Deviation', 'Variance']) #initializes dataframe
    for point in alt:
        #appends each set of # of points, range, stdvar, and variance
        df.append(dict(zip(df.columns,
         [len(point), (np.max(np.array(point))-np.min(np.array(point))),
          np.std(point), np.var(point)])), ignore_index=True)
    return df

def xovers(sort_list, intersections):
    xovers = [] #initializes an empty array to store crossovers
    for intr in intersections:
        points = [] #initializes an array to store points at a crossover
        for df in sort_list:
            index = df.iloc[:,0].searchsorted(intr[0]) #gets ideal index
            if index == 0: #accounts for out of bounding box point placement
                lower = df.iloc[index,:] #sets lower bound of possible point
                pass
            else:
                lower = df.iloc[index-1,:] #sets lower bound of possible point
            if index >= len(df.iloc[:,0]):
                higher = df.iloc[index-1,:] #sets upper bound of possible point
                pass
            else:
                higher = df.iloc[index,:] #sets upper bound of possible point
            if np.absolute(np.sum(np.subtract(higher[0:2], intr))) < 20 \
             or np.absolute(np.sum(np.subtract(lower[0:2], intr))) < 20: # checks if distance is acceptable
                if np.absolute(np.sum(np.subtract(higher[0:2], intr))) > np.absolute(np.sum(np.subtract(lower[0:2], intr))):
                    points.append(lower) #appends lower if closer
                else:
                    points.append(higher) #appends higher if closer
        xovers.append(points) #appends points array to xovers
    return xovers


def xover_error(file):
    df_total = pd.read_csv(file, header=None) #saves complete dataframe
    df_list = [group for _, group in df_total.groupby(3)] #separates dataframe by ground track
    line_list = [stats.linregress(df.iloc[:,0],df.iloc[:,1])[0:2] for df in df_list] #creates a list of regression lines
    intersections = solve(line_list, [np.min(np.array(df_total.iloc[:,0])), \
     np.max(np.array(df_total.iloc[:,0])), np.max(np.array(df_total.iloc[:,1])), \
     np.min(np.array(df_total.iloc[:,1]))]) #finds potential intersections
    sorted_list = [df.sort_values(by=df.columns[0], kind='mergesort') for df in df_list] #sorts dataframes for binary search
    xover_list = xovers(sorted_list, intersections) #creates a list of crossovers
    error_data = get_error(xover_list) #creates a datframe of error
    new_name = os.path.splitext(file)[0] + "_crossover_error.csv" #modifies original filename
    error_data.to_csv(new_name, index=False) #saves csv to file of name new_name
    return error_data, new_name #returns saved dataframe and new filename

def main():
    input_length = len(sys.argv) #saves length of command line input
    if input_length <= 1:
        print ("please input a filepath") #gives error message for lack of input
    else:
        regex = sys.argv[1] #saves filename regex
        file_list = glob.glob(regex) #saves list of filenames

        i = 1 #variable for saving current position in list
        for file in file_list:
            output = xover_error(file) #saves new csv file and saves method output
            print ("Saved new csv file with path: " + output[1])
            print ("output {0} of {1}".format(i, len(file_list)))
            i+=1 #increases i to new index


if __name__ == "__main__":
    main()
