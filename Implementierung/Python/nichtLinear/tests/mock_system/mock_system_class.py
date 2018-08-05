from classes.signal_class import signal_class
from helpers.apply_transfer_function import apply_transfer_function
from helpers.apply_K import apply_K
from helpers.csv_helper import read_in_transfer_function_old_convention
from copy import copy


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
        from settings import mock_data_path
        from helpers.K_helper import create_mock_K

        self.__Uin = None
        self.__Uin_measured = None
        self.__Uout_measured = None
        self.__Uin_real = None
        self.__Uout_real = None
        self.__H = read_in_transfer_function_old_convention(mock_data_path + '/adjustH/Messung3/Ha_0.csv', mock_data_path + '/adjustH/Messung3/Hp_0.csv')
        self.__K = create_mock_K(points=999, linearVpp_in_mV=300, x_range_in_mV=1200, periods=1)

    # def get_Uout_from_Uin(self, Uin):
    #     self.__Uin = Uin
    #     self.__Uout_real = apply_transfer_function(self.__Uin, self.__H)
    #     self.__Uout_measured = signal_class(self.__Uout_real.in_V*0.5, self.__Uout_real.sample_rate)
    #     return self.__Uout_measured

    @property
    def H(self):
        return self.__H

    @H.setter
    def H(self, H):
        self.__H = H

    @property
    def K(self):
        return self.__K

    @K.setter
    def K(self, K):
        self.__K = K

    def write_to_AWG(self, signal, awg_Vpp, samplerateAWG=0, frequency=0 ):

        if samplerateAWG!=0 :
            self.__Uin = signal_class.gen_signal_from_sample_rate(signal=signal, sample_rate=samplerateAWG)
        elif frequency!=0 :
            self.__Uin = signal_class.gen_signal_from_f_rep(signal=signal, f_rep=frequency)

        self.__Uin.Vpp = awg_Vpp

        verbosity = 0
        if verbosity:
            print('==================================================')
            print('Sending to mock AWG')
            print('sample rate : ' + str(self.__Uin.sample_rate))
            print('frequency : ' + str(self.__Uin.f_rep))


    def read_from_DSO_resolution(self, samplerateOszi,  vpp_ch1, fmax, signal):
        time, dataUin, dataUout = self.read_from_DSO(samplerateOszi,  vpp_ch1, fmax, signal)
        return (time, dataUin, dataUout)

    def read_from_DSO(self, samplerateOszi,  vpp_ch1, fmax, signal):

        self.__Uin_measured = self.__Uin
        self.__Uin_measured.sample_rate = samplerateOszi

        use_apply_K = True
        if use_apply_K :
            _, Uquest = apply_K(K_x_to_y=self.__K, Ux=self.__Uin, verbosity=0)
        else:
            Uquest = copy(self.__Uin)

        self.__Uout_measured = apply_transfer_function(Uquest, self.__H)
        self.__Uout_measured.sample_rate = samplerateOszi

        time = self.__Uin_measured.time
        dataUin = self.__Uin_measured.in_V
        dataUout = self.__Uout_measured.in_V

        return (time, dataUin, dataUout)


