from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention, read_in_signal, read_in_signal_with_sample_rate
from helpers.apply_transfer_function import apply_transfer_function
from classes.signal_class import signal_class
from numpy.fft import fft, ifft
from numpy import floor
from numpy import concatenate





class mock_system_class :
    """
    """
    def __init__(self):
        from settings import mock_data_path

        self.__Uin = None
        self.__Uin_measured = None
        self.__Uout_measured = None
        self.__Uin_real = None
        self.__Uout_real = None
        self.__H = read_in_transfer_function_old_convention(mock_data_path + '/adjustH/Messung3/Ha_0.csv', mock_data_path + '/adjustH/Messung3/Hp_0.csv')

        ############
        folder_transfer_function = mock_data_path + 'get_H/30.07.2018_09_09_52/csv/'

        path_transfer_funciton_ampl = folder_transfer_function + 'HAmpl_linear.csv'
        path_transfer_funciton_phase = folder_transfer_function + 'PhaseH.csv'

        self.__H = read_in_transfer_function_old_convention(path_transfer_funciton_ampl, path_transfer_funciton_phase, delimiter=';')
        ############
        # self.__H = read_in_transfer_function(mock_data_directory + '/H_jens.csv')

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

    def write_to_AWG(self, signal, awg_Vpp, samplerateAWG=0, frequency=0 ):

        from settings import mock_data_path

        if samplerateAWG!=0 :
            self.__Uin = signal_class.gen_signal_from_sample_rate(signal=signal, sample_rate=samplerateAWG)
        elif frequency!=0 :
            self.__Uin = signal_class.gen_signal_from_f_rep(signal=signal, f_rep=frequency)

        self.__Uin.Vpp = awg_Vpp

        ############
        folder_signal_ideal = mock_data_path + 'get_H/30.07.2018_09_09_52/csv/'

        path_Uin_vector = folder_signal_ideal + 'OriginalSignal.csv'
        path_Uin_sample_rate = folder_signal_ideal + 'Samplerates.csv'

        self.__Uin = read_in_signal_with_sample_rate(path_Uin_vector, path_Uin_sample_rate, delimiter=';')

        self.__Uin.Vpp = 40e-3
        ############

        print('==================================================')
        print('Sending to mock AWG')
        print('sample rate : ' + str(self.__Uin.sample_rate))
        print('frequency : ' + str(self.__Uin.f_rep))


    def read_from_DSO_resolution(self, samplerateOszi,  vpp_ch1, fmax, signal):
        time, dataUin, dataUout = self.read_from_DSO(samplerateOszi,  vpp_ch1, fmax, signal)
        return (time, dataUin, dataUout)

    def read_from_DSO(self, samplerateOszi,  vpp_ch1, fmax, signal):

        from helpers.plot_helper import plot_2_signals, plot_vector

        self.__Uin_real = self.__Uin
        self.__Uin_real.sample_rate = samplerateOszi

        Uin_vector = self.__Uin_real.in_V * 0.5

        self.__Uin_measured = signal_class(self.__Uin_real.time , Uin_vector  )

        self.__Uout_real = apply_transfer_function(self.__Uin, self.__H)



        self.__Uout_real.sample_rate = samplerateOszi

        Uout_vector = self.__Uout_real.in_V

        do_ifftfft = 0
        if do_ifftfft:
            Uout_vector_fft = fft(Uout_vector)
            lngth = int(floor(len(Uout_vector_fft)/2/2))
            faktor = len(Uout_vector_fft)/2 / lngth
            shorten = int(floor(len(Uout_vector_fft)/2/2))
            Uout_vector_fft_shorted = concatenate((Uout_vector_fft[0:shorten+1], Uout_vector_fft[-shorten:]))
            Uout_vector = ifft(Uout_vector_fft_shorted, n=len(Uout_vector)) / faktor

        Uout_vector = Uout_vector * 0.5

        self.__Uout_measured = signal_class.gen_signal_from_f_rep( Uout_vector, self.__Uout_real.f_rep )
        self.__Uout_measured.sample_rate = samplerateOszi

        time = self.__Uin_measured.time
        dataUin = self.__Uin_measured.in_V
        dataUout = self.__Uout_measured.in_V

        return (time, dataUin, dataUout)


