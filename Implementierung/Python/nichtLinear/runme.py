from evaluate_adjust_H import evaluate_adjust_H
from evaluate_with_BBsignal import evaluate_with_BBsignal
from helpers.plot_helper import plot_2_transfer_functions, plot_H_ideal_Hs, plot_2_signals
from settings import number_iterations


# Uout_ideal, Uout_measured, H_development = evaluate_adjust_H(number_iterations)

Uout_ideal, Uout_measured = evaluate_with_BBsignal()







# verbosity = 1
# if verbosity:
#     from settings import mock_system
#     H = mock_system.H
#     plot_H_ideal_Hs(H, H_development)
#     plot_2_signals(Uout_ideal, Uout_measured, legend1='Uout_ideal', legend2='Uout_measured')

