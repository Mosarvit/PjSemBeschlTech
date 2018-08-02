import csv
from numpy import genfromtxt

from classes.transfer_function_class import transfer_function_class
from classes.signal_class import signal_class
from helpers.other_helpers import get_current_method_name
import os



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

def save_1_col(filename, col):

    """

    save_1_col speichert einen vektor als CSV ab

    INPUT:

        filename : string; Dateipfad, wo abgespeichert werden soll
        col: nx1 vector; erste Spalte (n - länge des Vektors)

    OUTPUT:

        (no output)

    """

    with open(filename, 'w+', newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0, col.shape[0]):
            writer.writerow([str(col[i])])

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

def read_in_transfer_function_old_convention(pathA, pathPh, delimiter=','):
    Ha = genfromtxt(pathA, delimiter=delimiter)
    Hph = genfromtxt(pathPh, delimiter=delimiter)
    f = Ha[:, 0]
    H = transfer_function_class(f)
    H.a = Ha[:, 1]
    H.p = Hph[:, 1]
    return H

def read_in_transfer_function_complex(path, delimiter=','):
    H_compl = genfromtxt(path, delimiter=delimiter)
    H = transfer_function_class(H_compl[:, 0])
    H.c = H_compl[:, 1]
    return H


def read_in_K(path, delimiter=','):
    K = genfromtxt(path, delimiter=delimiter)
    return K


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

def save_transfer_function_old_convention(H, directory, id ):


    save_2cols(directory + '/Ha_' + str(id) + '.csv', H.f, H.a)
    save_2cols(directory + '/Hp_' + str(id) + '.csv', H.f, H.p)
    save_transfer_function(H, directory + '/H_' + str(id) + '.csv')



def read_in_signal(path, delimiter=','):

    U_old_convention = genfromtxt(path, delimiter=delimiter)
    U = signal_class(U_old_convention[:, 0], U_old_convention[:, 1])

    return U

def read_in_array(path, delimiter=','):
    array = genfromtxt(path, delimiter=delimiter)
    return array

def save_signal(signal, filename):
    save_2cols(filename, signal.time, signal.in_V)

def save_a(a, filename):
    save_1_col(filename, a)

def save_K(K, filename):
    save_2cols(filename, K[:,0], K[:,1])

def read_in_signal_with_sample_rate(path_signal, path_sample_rate, delimiter=','):

    U_vector = genfromtxt(path_signal, delimiter=delimiter)
    sample_rate = genfromtxt(path_sample_rate, delimiter=delimiter)
    U = signal_class.gen_signal_from_sample_rate(U_vector, sample_rate[1,1])

    return U

def read_in_get_H_signal_data(get_H_csv_directory):
    path_Uin_AWG_time = get_H_csv_directory + 'OriginalSignal.csv'
    path_Uin_sample_rate = get_H_csv_directory + 'Samplerates.csv'
    path_Uin_measured = get_H_csv_directory + 'UinTime.csv'
    path_Uout_time = get_H_csv_directory + 'UoutTime.csv'
    path_Uout_Ampl = get_H_csv_directory + 'UoutAmplFrq_linear.csv'
    path_Uout_Phase = get_H_csv_directory + 'UoutPhase.csv'
    path_Uin_Ampl = get_H_csv_directory + 'UinAmplFrq_linear.csv'
    path_Uin_Phase = get_H_csv_directory + 'UinPhase.csv'
    path_Ha = get_H_csv_directory + 'HAmpl_linear.csv'
    path_Hp = get_H_csv_directory + 'PhaseH.csv'
    Uin_AWG = read_in_signal_with_sample_rate(path_Uin_AWG_time, path_Uin_sample_rate, delimiter=';')
    Uin_time_measured = read_in_signal(path_Uin_measured, delimiter=';')
    Uout_time_measured = read_in_signal(path_Uout_time, delimiter=';')
    Uout_freq_measured = read_in_transfer_function_old_convention(pathA=path_Uout_Ampl, pathPh=path_Uout_Phase,
                                                                  delimiter=';')
    Uin_freq_measured = read_in_transfer_function_old_convention(pathA=path_Uin_Ampl, pathPh=path_Uin_Phase,
                                                                 delimiter=';')
    H = read_in_transfer_function_old_convention(pathA=path_Ha, pathPh=path_Hp, delimiter=';')

    return Uin_AWG, Uin_time_measured, Uout_time_measured, Uout_freq_measured, Uin_freq_measured, H

def load_ideal_signal(filename, datatype):
    ideal_values_data_path, current_unit_test_data_path = generate_paths_for_ideal_values(filename)
    if not os.path.exists(ideal_values_data_path):
        raise CustomValueError("No ideal signal found. You should first set the ideal signal by setting argument set_ideal_signal in method finilize_test_with_signal to True")
    if datatype == 'signal':
        values_ideal = read_in_signal(ideal_values_data_path)
    elif datatype == 'transfer_function':
        values_ideal = read_in_transfer_function(ideal_values_data_path)
    elif datatype == 'a' or datatype == 'K':
        values_ideal = read_in_array(ideal_values_data_path)
    else :
        raise CustomValueError("Unknown datatype")

    return values_ideal

def save_ideal_signal(signal_ideal, filename, datatype):
    ideal_values_data_path, current_unit_test_data_path = generate_paths_for_ideal_values(filename)
    if not os.path.exists(current_unit_test_data_path):
        os.makedirs(current_unit_test_data_path)
    if datatype == 'signal':
        save_signal(signal_ideal, ideal_values_data_path)
    elif datatype == 'transfer_function':
        save_transfer_function(signal_ideal, ideal_values_data_path)
    elif datatype == 'a':
        save_a(signal_ideal, ideal_values_data_path)
    elif datatype == 'K':
        save_K(signal_ideal, ideal_values_data_path)
    else:
        raise CustomValueError("Unknown datatype")

def load_ideal_a(filename):

    ideal_values_data_path, current_unit_test_data_path = generate_paths_for_ideal_values(filename)
    if not os.path.exists(ideal_values_data_path):
        raise CustomValueError("No ideal a found. You should first set the ideal signal by setting argument set_ideal_signal in method finilize_test_with_signal to True")
    a_ideal = read_in_a(ideal_values_data_path)
    return a_ideal

def save_ideal_a(a_ideal, filename):
    a_ideal_data_path, current_unit_test_data_path = generate_paths_for_ideal_values(filename)
    if not os.path.exists(current_unit_test_data_path):
        os.makedirs(current_unit_test_data_path)
    save_a(a_ideal, a_ideal_data_path)


def generate_paths_for_ideal_values(filename):
    from settings import test_data_path
    current_unit_test_data_path = test_data_path + get_current_method_name(4) + '/'
    Uout_ideal_data_path = current_unit_test_data_path + filename
    return Uout_ideal_data_path, current_unit_test_data_path

class CustomValueError(ValueError):
 def __init__(self, arg):
  self.strerror = arg
  self.args = {arg}
