from helpers.csvHelper import read_in_transfer_function
from helpers.apply_transfer_function import apply_transfer_function
from classes.signal_class import signal_class
import global_data


class mock_system_class :

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
        self.__Uin_measured = None
        self.__Uout_measured = None
        self.__Uin_real = None
        self.__Uout_real = None
        self.__H = read_in_transfer_function(global_data.project_path + '/tests/mock_data/H_jens.csv')

    # def get_Uout_from_Uin(self, Uin):
    #     self.__Uin = Uin
    #     self.__Uout_real = apply_transfer_function(self.__Uin, self.__H)
    #     self.__Uout_measured = signal_class(self.__Uout_real.in_V*0.5, self.__Uout_real.sample_rate)
    #     return self.__Uout_measured

    def write_to_AWG(self, Uin):
        self.__Uin = Uin

        frequency = self.__Uin.sample_rate / len(self.__Uin.time)
        print('Sending to AWG')
        print('signal length : ' + str(len(self.__Uin.time) ))
        print('sample rate : ' + str(self.__Uin.sample_rate))
        print('frequency : ' + str(frequency))

    def read_from_DSO(self):
        self.__Uin_real = self.__Uin
        self.__Uin_measured = signal_class(self.__Uin_real.time , self.__Uin_real.in_V * 0.5, )
        self.__Uout_real = apply_transfer_function(self.__Uin, self.__H)
        self.__Uout_measured = signal_class(self.__Uout_real.time, self.__Uout_real.in_V * 0.5 )
        return (self.__Uin_measured, self.__Uout_measured)


