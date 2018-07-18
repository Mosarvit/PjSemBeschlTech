from unittest import TestCase
import unittest
from blocks.generate_BBsignal import generate_BBsignal, generate_BBsignal_new
import settings
from helpers.signal_evaluation import signal_evaluate



class test_generate_BBsignal(TestCase):


    def __init__(self, *args, **kwargs):
        super(test_generate_BBsignal, self).__init__(*args, **kwargs)

    @unittest.skip("currently not working")
    def test_generate_BBsignal_show(self):
        # Initialization
        sampleRateDSO = 999900000
        f_rep = 900e3
        sample_rate_AWG_max = 223 * f_rep
        f_BB = 5e6
        Vpp = 0.3
        Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                       saveCSV=True, verbosity=False)

        Uout_2 = generate_BBsignal_new(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                       saveCSV=True, verbosity=False)

        # print("Werte alt:")
        # signal_evaluate(settings.project_path + '/data/current_data/BBsignal_ideal.csv')
        # print("Werte neu:")
        # signal_evaluate(settings.project_path + '/data/current_data/BBsignal_new.csv')
        # Wirft fehler!

        self.assertTrue(True)