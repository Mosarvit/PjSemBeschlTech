import numpy as np

class transfer_function :

    """
    transfer_function is a class, that describes a transfer function
    Initialization :
        pass the frequency vector:
        H = transfer_function(frequency)
    Getters:
        H.f - get frequency
        H.a - get amplitude
        H.p - get phase shift
        H.c - get complex amplification
    Setter:
        H.a_p - set amplitude and phase shift, can only be set together
        H.c -   set complex amplification
        frequency cannot be set
    """
    def __init__(self, frequency):
        self.__frequency = frequency
        self.__amplitude = None
        self.__phaseshift = None
        self.__complex = None

    @property
    def f(self):
        return self.__frequency

    @property
    def a(self):
        return self.__amplitude

    @property
    def p(self):
        return self.__phaseshift

    @property
    def c(self):
        return self.__complex

    @p.setter
    def a_p(self, vals):
        apm, ph = vals
        self.__amplitude = apm
        self.__phaseshift = ph
        self.__complex = self.__amplitude * (np.cos(self.__phaseshift) + 1j * np.sin(self.__phaseshift))

    @c.setter
    def c(self, value):
        self.__complex = value
        self.__amplitude = np.abs(self.__complex)
        self.__phaseshift = np.angle(self.__complex)


Ha = np.zeros([5,1])
H = transfer_function(Ha)
# H.a_p = Ha[:, 1], Hph[:,0]
