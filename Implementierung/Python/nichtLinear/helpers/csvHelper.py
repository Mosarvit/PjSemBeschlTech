import csv
from numpy import genfromtxt
import numpy as np
from adts.transfer_function import transfer_function

def save_2cols(filename, col1, col2):

    """

    save_2cols speichert zwei vektoren gleicher Länge als CSV ab

    INPUT:

        filename : string; Dateipfad, wo abgespeichert werden soll
        col1: nx1 vector; erste Spalte (n - länge des Vektors)
        col2 : nx1 vector; zweite Spalte (n - länge des Vektors)

    OUTPUT:

        (no output)

    """

    with open(filename, 'w+', newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0, col1.shape[0]):
            writer.writerow([str(col1[i]), str(col2[i])])

def read_in_H(pathA, pathPh):
    Ha = genfromtxt(pathA, delimiter=',')
    Hph = genfromtxt(pathPh, delimiter=',')
    H = np.zeros(((Ha.shape[0]), 3))
    H[:, 0:2] = Ha
    H[:, 2] = Hph[:, 1]
    return H

def read_in_transfer_function(pathA, pathPh):
    Ha = genfromtxt(pathA, delimiter=',')
    Hph = genfromtxt(pathPh, delimiter=',')
    H = transfer_function(Ha[:,0])
    H.a = Ha[:, 1]
    H.p = Hph[:, 1]
    return H