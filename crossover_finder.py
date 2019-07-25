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

     # [a1, a2] where each is a point [x1, y1]
    intersects = []

    for i in line_list:
        for j in line_list:
            # if lines are different and have opposing slopes
            if i != j and i[0]*j[0] < 0:  #assuming slope is index 0
                intersects.append(get_intersect(i, j))
        line_list.remove(i)

    for i in intersects:
        if i[0] > box[0] or i[1] > box[2] or i[0] < box[3] or i[1] < box[1]: #checks if point is out of range
            #intersects.remove(i)
            pass


    return set(intersects)


def get_intersect(point1, point2):
    # slope/intercept form => [slope, intercept]
    x = round( (point2[1]-point1[1]) / (point1[0]-point2[0]) , 3)
    y = round( point1[0]*x + point1[1] , 3)
    return ( x,y)


def get_error(alt):
    df = pd.DataFrame(columns=['Number of Points', 'Range',
     'Standard Deviation', 'Variance']) #initializes dataframe
    for point in alt:
        #appends each set of # of points, range, stdvar, and variance
        if len(point) > 0:
            df = df.append(dict(zip(df.columns,
             [len(point), (np.max(np.array(point))-np.min(np.array(point))),
              np.std(point), np.var(point)])), ignore_index=True)
    return df

def magn(vector):
    for i in range(len(vector)):
        if vector[i] is None or vector[i] == np.inf or vector[i] == np.NINF:
            vector[i] = 0
    mag = np.sqrt(vector.dot(vector))
    return mag

def lerp(lower, higher, intr):
    diff = np.subtract(higher, lower)
    if np.prod(diff[0:2]) == 0:
        return None
    magdiff = magn(diff[0:2])
    intr_diff = np.subtract(intr, lower[0:2])
    magintr = magn(intr_diff)
    mag = magintr/magdiff
    if mag>1:
        return None
    lerped = np.add(lower, mag * diff)
    veri_diff = np.absolute(np.subtract(intr, lerped[0:2]))
    veri = np.sqrt(veri_diff.dot(veri_diff))
    #print("lower: ({0},{1}), higher: ({2},{3}), intr: ({4},{5}), veri: {6}".format(lower[0], lower[1], higher[0], higher[1], intr[0], intr[1], veri))
    if veri < 50:
        return lerped[2]
    return None

def xovers(sort_list, line_list, intersections):
    xovers = [] #initializes an empty array to store crossovers
    for intr in intersections:
        points = [] #initializes an array to store points at a crossover
        for df in sort_list:
            index = df.iloc[:,0].searchsorted(intr[0]) #gets ideal index
            if index == 0: #accounts for out of bounding box point placement
                lower = df.iloc[index,:] #sets lower bound of possible point
            else:
                lower = df.iloc[index-1,:] #sets lower bound of possible point
            if index >= len(df.iloc[:,0]):
                higher = df.iloc[index-1,:] #sets upper bound of possible point
            else:
                higher = df.iloc[index,:] #sets upper bound of possible point
            #print("ideal x: {0}, low x: {1}, high x: {2}".format(intr[0], lower[0], higher[0]))
            l = lerp(lower, higher, intr)
            if l is not None:
                points.append(l)
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
    xover_list = xovers(sorted_list, line_list, intersections) #creates a list of crossovers
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
