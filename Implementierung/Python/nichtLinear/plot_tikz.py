import matplotlib.pyplot as plt
import numpy as np
from matplotlib2tikz import save as tikz_save
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


# example data
x = np.arange(0.1, 4, 0.5)
y = np.exp(-x)

# example error bar values that vary with x-position
error = 0.1 + 0.2 * x

fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
ax0.errorbar(x, y, yerr=error, fmt='-o')
ax0.set_title('\label{fig:Nolte} erster Plot')

# error bar values w/ different -/+ errors that
# also vary with the x-position
lower_error = 0.4 * error
upper_error = error
asymmetric_error = [lower_error, upper_error]

ax1.errorbar(x, y, xerr=asymmetric_error, fmt='o')
ax1.set_title('variable, asymmetric error')
ax1.set_yscale('log')

tikz_save('/Users/max/GitHub/PjSemBeschlTech/ErstellteDokumente/Report/latex_main/images/plots/second.tikz', figureheight = '\\figureheight', figurewidth = '\\figurewidth')
plt.show()