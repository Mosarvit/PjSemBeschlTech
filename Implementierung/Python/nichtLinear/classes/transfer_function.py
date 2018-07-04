import numpy as np
import copy
from scipy import linalg

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

        # phaseshift = np.angle(self.__complex)

        PhaseH = np.asarray([float(i) for i in np.angle(self.__complex)])
        PhaseVGL = np.asarray([float(i) for i in np.angle(self.__complex)])

        for ind in range(0, (len(PhaseH) - 1)):
            if PhaseVGL[ind] * PhaseVGL[ind + 1] < 0:
                if PhaseVGL[ind] > np.pi / 2 and PhaseVGL[ind + 1] < -np.pi / 2:
                    PhaseH[ind + 1:] = PhaseH[ind + 1:] + 2 * np.pi
                elif PhaseVGL[ind] < -np.pi / 2 and PhaseVGL[ind + 1] > np.pi / 2:
                    PhaseH[ind + 1:] = PhaseH[ind + 1:] - 2 * np.pi

        self.__phaseshift = PhaseH

    def update_complex(self):
        self.__complex = self.__amplitude * (np.cos(self.__phaseshift) + 1j * np.sin(self.__phaseshift))

    def get_inverse(self):
        Hinv = transfer_function(self.f)
        Hinv.c = 1/self.c
        return Hinv