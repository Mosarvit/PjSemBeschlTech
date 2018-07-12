import csv
from numpy import genfromtxt

from classes.transfer_function_class import transfer_function_class
from classes.signal_class import signal_class


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
    H = transfer_function_class(Ha[:, 0])
    H.a = Ha[:, 1]
    H.p = Ha[:, 2]
    return H

def read_in_transfer_function_old_convention(pathA, pathPh):
    Ha = genfromtxt(pathA, delimiter=',')
    Hph = genfromtxt(pathPh, delimiter=',')
    H = transfer_function_class(Ha[:, 0])
    H.a = Ha[:, 1]
    H.p = Hph[:, 1]
    return H

def save_transfer_function(H, directory, id ):

    """

    save_transfer_function save an inctance of class transfer_function as CSV

    INPUT:

        filename : string; Dateipfad, wo abgespeichert werden soll
        H: an inctance of class transfer_function

    OUTPUT:

        (no output)

    """
    filename = directory + '/H_' + str(id) + '.csv'
    with open(filename, 'w+', newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0, H.f.shape[0]):
            writer.writerow([str(H.f[i]), str(H.a[i]), str(H.p[i]), str(H.c[i])])

def save_transfer_function_old_convention(H, directory, id ):


    save_2cols(directory + '/Ha_' + str(id) + '.csv', H.f, H.a)
    save_2cols(directory + '/Hp_' + str(id) + '.csv', H.f, H.p)
    save_transfer_function(H, directory + '/H_' + str(id) + '.csv')

def read_in_signal(file):



    U_old_convention = genfromtxt(file, delimiter=',')
    # sample_rate = int(np.round(1 / (U_old_convention[1, 0] - U_old_convention[0, 0])))
    # sample_rate = int(np.round((U_old_convention.shape[0] - 1) / (U_old_convention[-1, 0] - U_old_convention[0, 0])))
    # U = signal_class(signal_in_V=U_old_convention[:, 1], sample_rate=sample_rate)
    U = signal_class.gen_signal_from_old_convention(U_old_convention[:,0], U_old_convention[:,1])

    return U

def save_signale(signal, filename):
    save_2cols(filename, signal.time, signal.in_V)
