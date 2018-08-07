import matplotlib.pyplot as plt
import numpy as np
from matplotlib2tikz import save as tikz_save
from blocks.compute_a_from_Uin_Uquet import *
from blocks.compute_K_from_a import *
#from helpers.plot_helper import *
from helpers.csv_helper import *
from settings import *

# U1 = read_in_signal(project_path + 'data/optimizer/adjust_a_19_07_2018-13_54_54/Uquest_ideal_2.csv')
# plt.figure()
# plt.plot([t*1e6 for t in U1.time], U1.in_mV, 'r')
# plt.legend(['$U_?(t)$'])
# plt.xlabel('t in \si{\\micro \\second}')
# plt.ylabel('U in \si{\\milli \\volt}')
# #plt.grid(True)
#
# tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/first.tikz', figureheight = '\\figureheight', figurewidth = '\\figurewidth')

def adjust_a_plot_K():
    data_path = project_path + 'data/optimizer/adjust_a_19_07_2018-13_57_54/'
    plt.figure()

    Uquest_1_5 = read_in_signal(data_path + 'Uin_awg_1.csv')
    K0 = genfromtxt(data_path + 'K_initial.csv', delimiter=',')
    K1 = genfromtxt(data_path + 'K_1.csv', delimiter=',')
    K2 = genfromtxt(data_path + 'K_2.csv', delimiter=',')
    K3 = genfromtxt(data_path + 'K_3.csv', delimiter=',')
    K4 = genfromtxt(data_path + 'K_4.csv', delimiter=',')
    # evaluate adjust a mit Out vpp 1.5 V zurückgerechnet
    plt.plot(K0[:, 0][::2], K0[:, 1][::2], K1[:, 0][::2], K1[:, 1][::2], K2[:, 0][::2], K2[:, 1][::2])

    plt.legend(['$K_0$', '$K_1$', '$K_2$'])
    plt.xlabel('$U_{in}$ in \si{\\milli \\volt}')
    plt.ylabel('$U_{?}$ in \si{\\milli \\volt}')

    #plt.subplots_adjust(hspace=0.5)
    # tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/adjust_a_K.tikz', figureheight = '\\figureheight', figurewidth = '\\figurewidth')
    plt.show()

# def adjust_a_plot_Uin():
#     data_path = project_path + 'data/optimizer/adjust_a_19_07_2018-13_57_54/'
#     plt.figure()
#     # evaluate adjust a mit Out vpp 1.5 V zurückgerechnet
#     # plot vonUin
#     Uquest_1_5 = read_in_signal(data_path + 'Uin_awg_1.csv')
#     Uin_1 = read_in_signal(data_path + 'Uin_awg_2.csv', delimiter=',')
#     Uin_2 = read_in_signal(data_path + 'Uin_awg_3.csv', delimiter=',')
#     # Uin_2 = read_in_signal(data_path + 'Uin_measured_2.csv', delimiter=',')
#     plt.plot([t * 1e6 for t in Uin_1.time], Uin_1.in_mV, [t * 1e6 for t in Uquest_1_5.time], Uquest_1_5.in_mV, [t * 1e6 for t in Uin_2.time], Uin_2.in_mV)
#
#     plt.legend(['$U_{in,1}$', '$U_{?,0}$', '$U_{in,2}$'])
#     plt.xlabel('$t$ in \si{\\micro \\second}')
#     plt.ylabel('$U_{in}$ in \si{\\milli \\volt}')
#
#     # tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/adjust_a_Uin.tikz', figureheight = '\\figureheight', figurewidth = '\\figurewidth')
#     plt.show()
#
# def adjust_a_plot_Uin_K():
#     data_path = project_path + 'data/optimizer/adjust_a_19_07_2018-13_57_54/'
#     plt.figure()
#
#     K0 = genfromtxt(data_path + 'K_initial.csv', delimiter=',')
#     K1 = genfromtxt(data_path + 'K_1.csv', delimiter=',')
#     # evaluate adjust a mit Out vpp 1.5 V zurückgerechnet
#     plt.subplot(1, 2, 1)
#     plt.plot(K0[:, 0], K0[:, 1], K1[:, 0], K1[:, 1])
#     plt.legend(['$K_0$', '$K_1$', '$K_2$'])
#     plt.xlabel('$U_{in}$ in \si{\\milli \\volt}')
#     plt.ylabel('$U_{?}$ in \si{\\milli \\volt}')
#
#     plt.subplot(1, 2, 2)
#     Uout_1 = read_in_signal(data_path + 'Uout_measured_1.csv', delimiter=',')
#     Uout_2 = read_in_signal(data_path + 'Uout_measured_2.csv', delimiter=',')
#     plt.plot([t * 1e6 for t in Uout_1.time[::4]], Uout_1.in_mV[::4], [t * 1e6 for t in Uout_2.time[::4]], Uout_2.in_mV[::4])
#     plt.legend(['$U_{out,0}$', '$U_{out,1}$'])
#     plt.xlabel('$t$ in \si{\\micro \\second}')
#     plt.ylabel('$U_{out}$ in \si{\\milli \\volt}')
#
#     # tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/adjust_a_Uout_K.tikz', figureheight = '\\figureheight', figurewidth = '\\figurewidth')
#     plt.show()

def adjust_a_plot_Uout():
    data_path = project_path + 'data/optimizer/adjust_a_19_07_2018-13_57_54/'
    plt.figure()
    # evaluate adjust a mit Out vpp 1.5 V zurückgerechnet
    # plot vonUin

    Uout_1 = read_in_signal(data_path + 'Uout_measured_1.csv', delimiter=',')
    Uout_2 = read_in_signal(data_path + 'Uout_measured_2.csv', delimiter=',')
    # plt.plot([t * 1e6 for t in Uout_1.time[::4]], Uout_1.in_mV[::4], [t * 1e6 for t in Uout_2.time[::4]],Uout_2.in_mV[::4])
    plt.plot([t * 1e6 for t in Uout_1.time[::100]], Uout_1.in_mV[::100], [t * 1e6 for t in Uout_2.time[::100]], Uout_2.in_mV[::100])
    plt.legend(['$U_{out,0}$', '$U_{out,1}$', '$U_{out,2}$'])
    plt.xlabel('$t$ in \si{\\micro \\second}')
    plt.ylabel('$U_{out}$ in \si{\\milli \\volt}')

    tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/adjust_a_Uout.tikz', figureheight='\\figureheight', figurewidth='\\figurewidth')
    plt.show()

def adjust_a_plot_Uquest():
    data_path = project_path + 'data/optimizer/adjust_a_19_07_2018-13_53_38/'
    plt.figure()
    # evaluate adjust a mit Out vpp 3,.. V zurückgerechnet
    # plot vonUin

    Uquest = read_in_signal(data_path + 'Uquest_initial.csv', delimiter=',')
    Uin = read_in_signal(data_path + 'Uin_initial.csv', delimiter=',')
    # H0 = read_in_transfer_function(data_path + 'H_0.csv')
    # K0 = genfromtxt(data_path + 'K_initial.csv', delimiter=',')

    a3 = compute_a_from_Uin_Uquet(Uin, Uquest, 3)
    K0 = compute_K_from_a(a3, verbosity=0)
    Uin = read_in_signal(data_path + 'Uin_initial.csv')
    #print(max(Uin.in_mV), min(Uin.in_mV))
    plt.plot(K0[:, 0][::2], K0[:, 1][::2])
    plt.legend(['$K_0$'], loc=2)
    plt.xlabel('$U_{in}$ in \si{\\milli \\volt}')
    plt.ylabel('$U_{?}$ in \si{\\milli \\volt}')
    plt.ylim((-400,400))
    Uout = read_in_signal(data_path + 'Uout_initial.csv', delimiter = ',')
    print(Uout.Vpp)

    # tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/K.tikz', figureheight='\\figureheight', figurewidth='\\figurewidth')
    plt.show()

    plt.plot([t * 1e6 for t in Uquest.time[::100]], Uquest.in_mV[::100], [t * 1e6 for t in Uin.time[::100]], Uin.in_mV[::100])
    plt.legend(['$U_{?,1}$', '$U_{in}$'])
    plt.xlabel('$t$ in \si{\\micro \\second}')
    plt.ylabel('$U$ in \si{\\milli \\volt}')
    plt.ylim((-400,400))
    # tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/UinUquest.tikz', figureheight='\\figureheight', figurewidth='\\figurewidth')
    plt.show()
# adjust_a_plot_Uquest()
# adjust_a_plot_Uin_K()
# adjust_a_plot_Uin() #sinnlos
# adjust_a_plot_K()
# adjust_a_plot_Uout()

def new_adjust_a_plot_K():
    data_path = project_path + 'data/evaluate_K_06_08_2018-12_59_03/'
    plt.figure()

    vpp_quality = genfromtxt(data_path + 'Vpp_quality.csv', delimiter=',')
    K0 = genfromtxt(data_path + 'K_initial.csv', delimiter=',')
    Uquest5 = read_in_signal(data_path + 'Uquest_adapted_5.csv')
    Uquest9 = read_in_signal(data_path + 'Uquest_adapted_9.csv')
    # evaluate adjust a mit Out vpp 1.5 V zurückgerechnet
    Vpp_Kmax = K0[-1,1] - K0[0,1]
    vpp_quality[:,0] = [vpp*1000/Vpp_Kmax for vpp in vpp_quality[:,0]]
    Vpp_max = vpp_quality[-1,0]
    Vpp_min = vpp_quality[-2,0]
    # plt.subplot(1, 2, 1)
    plt.plot(K0[:, 0][::2], K0[:, 1][::2])
    plt.axhline(y=max(Uquest5.in_mV), color='r', linestyle='-')
    plt.axhline(y=min(Uquest5.in_mV), color='r', linestyle='-')
    plt.axhline(y=max(Uquest9.in_mV), color='g', linestyle='-')
    plt.axhline(y=min(Uquest9.in_mV), color='g', linestyle='-')


    plt.legend(['$K_0$'])
    plt.xlabel('$U_{in}$ in \si{\\milli \\volt}')
    plt.ylabel('$U_{?}$ in \si{\\milli \\volt}')
    tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/evaluate_K.tikz', figureheight='\\figureheight', figurewidth='\\figurewidth')

    plt.show()
    # plt.subplot(1, 2, 2)
    plt.plot(vpp_quality[:,0], vpp_quality[:,1], 'x')

    plt.legend(['Güte'])
    plt.xlabel('$\\frac{V_{PP, U_{?}}}{V_{PP, max}}$')
    plt.ylabel('QGesamt1')

    tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/evaluate_K_quality.tikz', figureheight='\\figureheight', figurewidth='\\figurewidth')

    plt.show()

new_adjust_a_plot_K()