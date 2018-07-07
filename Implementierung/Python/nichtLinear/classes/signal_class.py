import numpy as np
import copy
from scipy import linalg
from scipy.interpolate import interp1d
from helpers.signalHelper import find_nearest

class signal_class :

    def __init__(self, signal_in_V, sample_rate):
        self.__original_sample_rate = sample_rate
        self.__orginial_signal_in_V = signal_in_V
        orginial_Vpp = max(self.__orginial_signal_in_V) - min(self.__orginial_signal_in_V)
        self.__orginial_Vpp_normalized = self.__orginial_signal_in_V / orginial_Vpp

        self.__sample_rate = self.__original_sample_rate
        self.__signal_in_V = self.__orginial_signal_in_V
        self.__Vpp = max(signal_in_V) - min(signal_in_V)
        self.__time = None
        self.__t_end = None
        self.update_signal_in_mV()
        self.update_time()

    def update_time(self):
        if self.__t_end is None :
            self.__t_end = 1/self.__sample_rate * (len(self.__orginial_signal_in_V)-1)
            lngth = len(self.__orginial_signal_in_V)

        else :
            oldsr = 1 / (self.__time[1]-self.__time[0])
            lngth = int(np.round(((len(self.__time) - 1) / (oldsr) * (self.__sample_rate)) + 1))

        self.__time = np.linspace(0, self.__t_end, num=lngth, endpoint=True)

    def update_signal_in_mV(self):
        self.__signal_in_mV = self.__signal_in_V * 1000

    def update_signal(self):
        self.__signal_in_V = self.__orginial_Vpp_normalized * self.__Vpp
        self.update_signal_in_mV()

    @property
    def in_V(self):
        return self.__signal_in_V

    @property
    def in_mV(self):
        return self.__signal_in_mV

    @property
    def time(self):
        return self.__time

    @property
    def t_end(self):
        return self.__t_end

    @property
    def sample_rate(self):
        return self.__sample_rate

    @property
    def Vpp(self):
        return self.__Vpp

    @t_end.setter
    def t_end(self, t_end):
        self.__t_end = t_end
        self.update_time()  # todo : the signal should also be adjusted by interpolating

    @sample_rate.setter
    def sample_rate(self, new_sr):

        t_old = self.get_original_time()

        old_sr = self.__sample_rate
        self.__sample_rate = new_sr
        lngth = int(np.round(((len(self.__time) - 1)  / (old_sr ) * (new_sr ) ) + 1))
        self.__time = np.linspace(0, self.__t_end, num=lngth, endpoint=True)

        t_new = self.__time

        f = interp1d(t_old, self.__orginial_signal_in_V , bounds_error=False , fill_value = "extrapolate" )
        self.__signal_in_V = f(t_new)

        self.update_signal_in_mV()

    @Vpp.setter
    def Vpp(self, Vpp):
        self.__Vpp = Vpp
        self.update_signal()

    def get_original_time(self):
        t_end = 1 / self.__original_sample_rate * (len(self.__orginial_signal_in_V) - 1)
        t_length = len(self.__orginial_signal_in_V)
        time_original = np.linspace(0, t_end, num=t_length, endpoint=True)
        return time_original

    def get_signal_in_V_old_convention(self):
        U = np.zeros( [ len(self.__time), 2 ] )
        U[:, 0] = self.__time
        U[:, 1] = self.__signal_in_V
        return U

    def get_signal_in_mV_old_convention(self):
        U = np.zeros( [ len(self.__time), 2 ] )
        U[:, 0] = self.__time
        U[:, 1] = self.__signal_in_mV
        return U

    @staticmethod
    def gen_signal_from_old_convention(signal_old_convention):
        sample_rate = int(np.round(1 / (signal_old_convention[1, 0] - signal_old_convention[0, 0])))
        signal = signal_class(signal_old_convention[:, 1], sample_rate)
        return signal

    def cut_one_period(signal, f):

        T = 1 / f
        indT = find_nearest(signal.time, T + signal.time[0])
        signal_cut = signal_class(signal.in_V[0:indT], signal.sample_rate)

        return signal_cut

# U = np.array([ 0  ,  -2.25,  1.5 , 2 , 2   ])
# sample_rate = 4
# signal = signal_class(U, sample_rate)
#
# signal.sample_rate = 8
# signal.sample_rate = 4
#
# a=1