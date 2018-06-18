import numpy as np
def find1(array, value):

    """
    find_nearest findet den Index des Werts im vektor, der dem gesuchten Wert am nähsten liegt

    INPUT:
        array - der Vektor
        value - skalar; die gesuchte Zahl

    OUTPUT:
        idx - unsigned integer; der gesuchte Index
    """

    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx