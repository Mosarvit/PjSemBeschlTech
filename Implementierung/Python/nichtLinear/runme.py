from evaluate_adjust_H import evaluate_adjust_H
from helpers.plot_helper import plot_2_transfer_functions

Uout_ideal, Uout_measured, H_0, H_last = evaluate_adjust_H(3)

# hier stimmt was nicht mit den plots glaube ich MN
#plot_2_transfer_functions(H_0, H_last, 'H_0', 'H_last')

