from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.measure_H import measure_H
from blocks.measure_Uout import measure_Uout
from helpers.signalHelper import convert_V_to_mV
from helpers.signalHelper import convert_mV_to_V
from helpers.signalHelper import setVpp
from helpers.signalHelper import cut_one_period
from helpers.csvHelper import read_in_transfer_function
from global_data import project_path

import numpy as np


def evaluate_with_BBsignal(use_mock_system=0) :

    sampleRateAWG = 999900000
    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.3

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sampleRateAWG=sampleRateAWG, verbosity=0)

    if use_mock_system :
        H = read_in_transfer_function(project_path + '/tests/mock_data/H_jens.csv')
    else :
        H = measure_H(loadCSV=0, saveCSV=True, verbosity=1)
    
    
    Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)
    
    Uin = setVpp(Uquest_ideal, Vpp)
    
    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sampleRateAWG=sampleRateAWG, loadCSV=0, saveCSV=True, id='1', verbosity=0, use_mock_system=use_mock_system)
    
    # begin cut just one period out of Uout_measured

    Uout_measured = cut_one_period(Uout_measured, f_rep)
    
    # end
    # begin plot cut Uout

    # fig = plt.figure()
    # plt.plot(Uout_measured[:,0], Uout_measured[:,1])
    # plt.title('Uout_measured')
    # plt.xlabel('t')
    # plt.ylabel('U')
    # if globalVars.showPlots :
    #     plt.show()
    # fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/Uout_measured_cut.pdf')

    # end

    Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
    Uquest_measured_mV = convert_V_to_mV(Uquest_measured)
    
    Uin_mV = convert_V_to_mV(Uin)

    a = compute_a_from_Uin_Uquet(Uin=Uin_mV, Uquest=Uquest_measured_mV, N=3)
    K = compute_K_from_a(a=a, verbosity=0)
    
    Uquest_ideal_mV = convert_V_to_mV(Uquest_ideal)

    Uin_mV = compute_Uin_from_Uquest(Uquest=Uquest_ideal_mV, K=K, verbosity=0)

    Uin = convert_mV_to_V(Uin_mV)

    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sampleRateAWG=sampleRateAWG, loadCSV=False, saveCSV=True, id='2', verbosity=0, use_mock_system=use_mock_system)

    return Uout_ideal, Uout_measured