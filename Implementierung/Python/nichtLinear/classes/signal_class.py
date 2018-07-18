import numpy as np
import copy
from scipy import linalg
from scipy.interpolate import interp1d
from helpers.signal_helper import find_nearest

class signal_class :
    """
        signal_class is a class, that describes a signal in time-domain.

        Initialization :
            from classes.signal_class import signal_class
            pass the time and signal (in V) vectors :
            U = signal_class( time, u_in_V )
        Getters:
            U.time          - get time vector
            U.in_V          - get signal vector in V
            U.in_mV         - get signal vector in mV
            U.sample_rate   - get sample rate
            U.Vpp           - get Vpp
            U.length        - get length of the signal
            U.timestep      - get the timestep between the first two values
            U.f_rep         - get the repetition frequency of the signal
        Setters:
            U.sample_rate   - set sample rate
            U.Vpp           - set Vpp

        * Setting a different time vector or a different signal vector is technically not meaningful, therefore such
        setters were not implemented.


        Example of initializing a transfer_function with amplitude and phaseshift:
            t = np.array([1,2,3,4,5])
            u_vector_inV = np.array([1,0,-1,-2,3])
            U = signal_class(t, u_vector_inV)

            The sample rate, repetition frequency and timestep of the signal are only useful
        if the time axis is evenly spaced. Then, the named values are given by
            - timestep = time[1] - time[0]
            - f_rep = 1 / ( N * timestep) with N = Number of points
            - sample rate = N * f_rep = 1 / timestep
        (comment: this includes, that the highest value in the time axis is given by (N-1)*timestep)
        """

    def __init__(self, time, signal_in_V):

        self.__orginal_signal_in_V = signal_in_V
        self.__orginal_time = time
        self.__timestep = time[1] - time[0]
<<<<<<< HEAD
        self.__original_sample_rate = 1 / (time[1] - time[0])
        self.__original_f_rep = self.__original_sample_rate / len(self.__orginal_signal_in_V)
=======
        self.__original_f_rep = 1 / (len(self.__orginal_time) * self.__timestep)
>>>>>>> 7e86cc36d7795b2099cd6051944d25f5b77a0836
        self.__original_sample_rate = len(signal_in_V)* self.__original_f_rep
        self.__orginial_Vpp = max(self.__orginal_signal_in_V) - min(self.__orginal_signal_in_V)
        self.__orginial_signal_normalized = self.__orginal_signal_in_V / self.__orginial_Vpp


        self.__sample_rate = self.__original_sample_rate
        self.__f_rep = self.__original_f_rep
        self.__signal_in_V = self.__orginal_signal_in_V
        self.__Vpp = self.__orginial_Vpp
        self.__time = self.__orginal_time


        self.update_signal_in_mV()

    def update_time(self):

        lngth = int(np.round(((len(self.__time) - 1) / (self.__original_sample_rate ) * (self.__sample_rate )))) + 1
        self.__time = np.linspace(0, self.__orginal_time[-1], num=lngth, endpoint=True)
        self.update_timestep()

    def update_timestep(self):
        self.__timestep = self.__time[1] - self.__time[0]

    def update_signal_in_mV(self):
        self.__signal_in_mV = self.__signal_in_V * 1000

    def update_signal(self):

        l_in = len(self.__orginal_time)
        l_out = len(self.__time)
        x_in = np.linspace(1, l_out, l_in)
        x_out = np.linspace(1, l_out, l_out)
        f = interp1d(x_in, self.__orginal_signal_in_V)

        self.__signal_in_V = f(x_out)

        self.update_Vpp()

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
        return self.__time[-1]

    @property
    def timestep(self):
        return self.__timestep

    @property
    def sample_rate(self):
        return self.__sample_rate

    @property
    def Vpp(self):
        return self.__Vpp

    @property
    def f_rep(self):
        return self.__f_rep

    @property
    def length(self):
        return len(self.time)

    @property
    def normalized(self):
        return self.__signal_in_V / (max(self.__signal_in_V) - min(self.__signal_in_V) )

    @sample_rate.setter
    def sample_rate(self, new_sr):

        self.__sample_rate = new_sr
        self.update_time()
        self.update_signal()
        self.__f_rep = self.__sample_rate / len(self.__signal_in_V)

    @Vpp.setter
    def Vpp(self, Vpp):
        self.__Vpp = Vpp
        self.update_Vpp()

    def update_Vpp(self):
        self.__signal_in_V = self.__signal_in_V / (max(self.__signal_in_V) - min(self.__signal_in_V)) * self.__Vpp
        self.update_signal_in_mV()

    def get_original_time(self):
        t_end = 1 / self.__original_sample_rate * (len(self.__orginal_signal_in_V) - 1)
        t_length = len(self.__orginal_signal_in_V)
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
    def gen_signal_from_sample_rate(signal, sample_rate):
        dt = 1/sample_rate
        time = np.linspace(0, dt*(len(signal)-1), len(signal), endpoint=True)

        signal = signal_class(time, signal)
        return signal

    @staticmethod
    def gen_signal_from_f_rep(signal_class_instance, f_rep):
        sample_rate = len(signal_class_instance) * f_rep
        signal_class_instance = signal_class.gen_signal_from_sample_rate(signal_class_instance, sample_rate)
        return signal_class_instance

    def cut_one_period(self, f, shift=0):

        T = 1 / f
        indT = find_nearest(self.time, T + self.time[0])
        b=indT
        signal_cut = signal_class( self.time[0:indT+1], self.in_V[shift:shift+indT+1])
        a0 = len(signal_cut.in_V)
        c0 = len(signal_cut.time)
        a1 = len(self.in_V)
        c1 = len(self.time)
#        signal_cut = signal_class( self.time[0:indT+1], self.in_V[0:indT+1])

        return signal_cut