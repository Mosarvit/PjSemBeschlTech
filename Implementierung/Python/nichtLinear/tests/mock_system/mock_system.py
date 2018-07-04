from numpy import genfromtxt
from helpers.csvHelper import read_in_transfer_function

class mock_system :

    """
    mock_system is a class, that describes a mock system for unit and system tests

    Initialization :
        pass the frequency vector:
        H = transfer_function(frequency)
    Getters:
        H.f - get frequency
        H.a - get amplitude
        H.p - get phase shift
        H.c - get complex amplification
    Setters:
        H.a(amplitude)  - set amplitude
        H.p(phase)      - set phase shift
        H.c(complex)    - set complex amplification

    Example of initializing a transfer_function with amplitude and phaseshift:
        f = np.array([1,2,3,4,5])
        H = transfer_function(f)
        H.a = 2*np.ones([5])
        H.p = 3*np.ones([5])

    Example of initializing a transfer_function as complex transfer function:
        f = np.array([1,2,3,4,5])
        H = transfer_function(f)
        H.c = 2 * np.ones(5) + 3j * np.ones(5)
    """
    def __init__(self):
        self.__Uin = None
        self.__Uout = None
        self.__H = read_in_transfer_function('mock_data/H_jens.csv')
        self.__K = genfromtxt('mock_data/a_300_jens.csv', delimiter=',')

    @property
    def Uin(self):
        return self.__Uin

    @property
    def Uout(self):
        return self.__Uout

    @Uin.setter
    def Uin(self, Uin):
        self.__Uin = Uin

    def get_Uout_from_Uin(self, Uin):
        self.__Uin = Uin



