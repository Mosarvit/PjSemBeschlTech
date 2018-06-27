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

# def read_in_H(pathA, pathPh):
#     Ha = genfromtxt(pathA, delimiter=',')
#     Hph = genfromtxt(pathPh, delimiter=',')
#     H = np.zeros(((Ha.shape[0]), 3))
#     H[:, 0:2] = Ha
#     H[:, 2] = Hph[:, 1]
#     return H

def read_in_transfer_function(path):
    Ha = genfromtxt(path, delimiter=',')
    H = transfer_function(Ha[:,0])
    H.a = Ha[:, 1]
    H.p = Ha[:, 2]
    return H

def read_in_transfer_function_old(pathA, pathPh):
    Ha = genfromtxt(pathA, delimiter=',')
    Hph = genfromtxt(pathPh, delimiter=',')
    H = transfer_function(Ha[:,0])
    H.a = Ha[:, 1]
    H.p = Hph[:, 1]
    return H

def save_transfer_function(H, filename):

    """

    save_transfer_function save an inctance of class transfer_function as CSV

    INPUT:

        filename : string; Dateipfad, wo abgespeichert werden soll
        H: an inctance of class transfer_function

    OUTPUT:

        (no output)

    """

    with open(filename, 'w+', newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0, H.f.shape[0]):
            writer.writerow([str(H.f[i]), str(H.a[i]), str(H.p[i]), str(H.c[i])])
