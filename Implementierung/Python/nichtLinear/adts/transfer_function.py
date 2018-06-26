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
    Setters:
        H.a_p - set amplitude and phase shift, can only be set together
        H.c -   set complex amplification
        frequency cannot be set

    Example of initializing a transfer_function with amplitude and phaseshift:
        f = np.array([1,2,3,4,5])
        H = transfer_function(f)
        H.a = 2*np.ones([5])
        H.p = 3*np.ones([5])

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
    def __init__(self, frequency):
        self.__frequency = frequency
        self.__amplitude = np.ones(len(frequency), dtype=float)
        self.__phaseshift = np.zeros(len(frequency), dtype=float)
        self.__complex = np.ones(len(frequency), dtype=complex) # 1 + j*0

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

    @a.setter
    def a(self, amplitude):
        self.__amplitude = amplitude
        self.update_complex()

    @p.setter
    def p(self, phase):
        self.__phaseshift = phase
        self.update_complex()

    @c.setter
    def c(self, value):
        self.__complex = value
        self.__amplitude = np.abs(self.__complex)
        self.__phaseshift = np.angle(self.__complex)

    def update_complex(self):
        self.__complex = self.__amplitude * (np.cos(self.__phaseshift) + 1j * np.sin(self.__phaseshift))