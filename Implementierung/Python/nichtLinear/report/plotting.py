
import matplotlib.pyplot as plt
from numpy import genfromtxt

def plotAndSave() :

    Uout_measured = genfromtxt('../data/current_data/Uout_1.csv', delimiter=',')

    plt.figure()
    plt.plot(Uout_measured[:,0],Uout_measured[:,1])
    plt.title('Uout_measured')
    plt.ylabel('u')
    plt.xlabel('t')

    plt.savefig('../../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/Uout_1.pdf')

plotAndSave()