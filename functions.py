# Functions for use in the main script

import numpy as np
import pandas as pd
from Annulus import annulus

def get_data(r, n, t = 1, method = "planar"):
    """ For the given 'r' and 'n', the function repeats the experiment 't' times
    It returns a dictionary of average values, except for probability, which will
    contain the probability.
    The keys for the dictionary are:
        - length
        - area
        - inclusion
        - probability
     """
    length_l = np.zeros(t)
    area_l = np.zeros(t)
    inclusion_l = np.zeros(t)
    for i in range(t):
        # Creates an annulus with radius r and n random points, generated by 'method'
        data = annulus(r, n, method)

        length_l[i] = data.hull_len
        area_l[i] = data.hull_area
        inclusion_l[i] = data.includes_circle

    length = length_l.mean()
    area = area_l.mean()
    inclusion = sum(inclusion_l)
    probability = inclusion_l.mean()

    # Dictionary of average values
    dictionary = {"length": length, "area": area, "inclusion": inclusion, "probability": probability}
    return dictionary


def create_data_matrix(r_array, n_array, times = 1, method = "polar"):
    """ Calls the get_data function and stores the calculated data in 2-dimensional arrays, which it will return,
    saved in a list. The 'times' parameter is for the get function
    The arrays are of (|n_array| x |r_array|) shape.
    The order of arrays in the returned list is:
        - length
        - area
        - inclusion
        - probability
    """
    shape = (len(r_array), len(n_array))
    length = np.zeros((shape))
    area = np.zeros((shape))
    inclusion = np.zeros((shape))
    probability = np.zeros((shape))

    for i in range(shape[0]):
        for j in range(shape[1]):
            r = r_array[i]
            n = n_array[j]
            data = get_data(r, n, times, method)
            # Saves the data into the appropriate slots in the array
            length[i, j] = data["length"]
            area[i, j] = data["area"]
            inclusion[i, j] = data["inclusion"]
            probability[i, j] = data["probability"]

    # Saves all of the arrays in a list.
    list_of_arrays = [length, area, inclusion, probability]
    return list_of_arrays


def save_to_csv(r_array, n_array, times = 1, method = "polar", NAME = ""):
    """ The function gets the data from the 'create_data_matrix' function.
    It extracts the arrays from the list (returned from the 'create_data_matrix')
    and saves them into a csv, named: type_method_times or type_method_times_NAME,
    depending whether or not a custom name was provided
    The separator in the csv is ','
    """
    data = create_data_matrix(r_array, n_array, times, method)

    names = ["length", "area", "inclusion", "probability"]
    col_names = np.hstack(("r", n_array))
    for i in range(len(names)):
        if NAME:
            name = "Data/{}_{}_{}_{}.csv".format(names[i], method, times, NAME)
        else:
            name = "Data/{}_{}_{}.csv".format(names[i], method, times)
        array = data[i]
        array = np.c_[r_array, array]
        array_df = pd.DataFrame(array, columns = col_names)
        array_df.to_csv(name, header=True, index = False)
    return
