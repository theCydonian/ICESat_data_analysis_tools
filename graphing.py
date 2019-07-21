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


# In order to use, you must have a local folder with all the csv data
# The command line should read 'python graphing.py <nameOfFolder>/<regexForFileNames>'
def main():
	file_list = list( glob.glob( sys.argv[1]  ) ) #file_list = list( glob.glob('Jakobshavn/jak_gla06_L[0-9][a-z]_[0-9]*_ascii.txt')) # saves list of filenames from regex
	df_list = []
	campaignAlts = {}
	for file in file_list:
		csv = 0
		try:
			csv = pd.read_csv( str( file) )
		except:
			continue
		df_list.append(csv) # adds each csv to the datframe list
        # Sort by time
		lat = csv.iloc[:,12]
        alt = csv.iloc[:,14]
        sol = csv.iloc[:,23]
        a_d = csv.iloc[:,6]
        coel = csv.iloc[:,144]
        campaign = str( csv.iloc[1,4] )
        campaignAlts.update(  { campaign : statistics.mean(alt) } )

        #Solar Angle Compairson Graphs
        plt.scatter(lat,alt,c=sol)
        cbar= plt.colorbar()
        cbar.set_label("solar angle")
        plt.savefig('Graphs/Jakobs_' + campaign + 'solAngle.png')
        plt.close()

        #Coelevation Comparison Graphs
        plt.scatter(lat,alt,c=coel)
        cbar= plt.colorbar()
        cbar.set_label("coelevation angle")
        plt.savefig('Graphs/Jakobs_' + campaign + 'coelevation.png')
        plt.close()

        """#Ascending/Descending Comparisons
        mapping = {'A': 'x', 'D': 'o'}
        for i in range(len(lat)):
            plt.scatter(lat[i], alt[i], marker=mapping[a_d[i]])
        plt.savefig('Graphs/Jakobs_' + campaign + 'asc_desc.png')
        plt.close()
        """

        #Scatterplots between solarAngle and altitude
        plt.scatter(lat,sol)
        plt.xlabel('latitude')
        plt.ylabel('solar angle')
        plt.savefig('Graphs/Jakobs_' + campaign + 'solScatter.png')
        plt.close()



    # Compare the average altitude of each laser
    values = list(campaignAlts.values())
    labels = list(campaignAlts.keys())
    plt.bar(range(len(campaignAlts)),values,tick_label=labels)
    plt.xlabel('laser campaigns')
    plt.ylabel('average altitude (m)')
    plt.savefig('Graphs/lasers.png')
    plt.close()

if __name__ == "__main__":
    main()

main()
