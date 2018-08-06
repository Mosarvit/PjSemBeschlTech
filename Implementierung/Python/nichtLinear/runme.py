from evaluate_adjust_H import evaluate_adjust_H
from helpers.plot_helper import plot_2_transfer_functions, plot_H_ideal_Hs, plot_2_signals

Uout_ideal, Uout_measured, H_development = evaluate_adjust_H(5, verbosity=1)

verbosity = 1
if verbosity:
    from settings import mock_system
    H = mock_system.H
    plot_H_ideal_Hs(H, H_development)
    plot_2_signals(Uout_ideal, Uout_measured, legend1='Uout_ideal', legend2='Uout_measured')

# hier stimmt was nicht mit den plots glaube ich MN
#plot_2_transfer_functions(H_0, H_last, 'H_0', 'H_last')

