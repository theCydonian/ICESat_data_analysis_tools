#geopandas_test.py
import numpy as np
import pandas as pd
import geopandas
import geoplot
import matplotlib.pyplot as plt
import os
import sys

def main():
    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    boroughs = geopandas.read_file(
        geoplot.datasets.get_path('nyc_boroughs')
    )
    collisions = geopandas.read_file(
        geoplot.datasets.get_path('nyc_injurious_collisions')
    )

    geoplot.polyplot(world, figsize=(8, 4))


if __name__ == "__main__":
    main()
