from evaluate_adjust_H import evaluate_adjust_H
from evaluate_adjust_a import evaluate_adjust_a
from evaluate_with_BBsignal import evaluate_with_BBsignal
from helpers.plot_helper import plot_2_transfer_functions, plot_H_ideal_Hs, plot_2_signals
from settings import number_iterations_H, number_iterations_K



Uout_ideal, Uout_measured = evaluate_with_BBsignal()
#Uout_ideal, Uout_measured, H_development = evaluate_adjust_H(number_iterations_H)
#Uout_ideal, Uout_measured, K = evaluate_adjust_a(number_iterations_K)


