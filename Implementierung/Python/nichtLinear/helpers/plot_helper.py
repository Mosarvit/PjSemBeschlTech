import matplotlib.pyplot as plt


def plot_vector(vector, legend='vektor'):
    plt.figure()
    plt.plot(vector)
    plt.legend([legend])
    plt.show()

def plot_2_signals(U1, U2, legend1='U1', legend2='U2'):
    plt.plot(U1.time, U1.in_V)
    plt.plot(U2.time, U2.in_V)
    plt.legend([legend1, legend2])
    plt.xlabel('t')
    plt.ylabel('U')
    plt.show()

def plot_transfer_function(H, legend='H'):
    plt.figure()
    plt.plot(H.f, H.a)
    plt.legend([legend])
    plt.xlabel('f')
    plt.ylabel('Amplitude')
    plt.show()

    plt.figure()
    plt.plot(H.f, H.p)
    plt.legend([legend])
    plt.xlabel('f')
    plt.ylabel('phase')
    plt.show()


def plot_2_transfer_functions(H1, H2,  legend1 = 'H1', legend2 = 'H2'):

    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(H1.f, H1.a, H2.f, H2.a, )
    axarr[0].legend([legend1, legend2])

    axarr[1].plot(H1.f, H1.p, H2.f, H2.p)
    axarr[1].legend([legend1, legend2])

    # if show_plots:
    plt.show()

def plot_3_transfer_functions(H1, H2, H3, legend1 = 'H1', legend2 = 'H2', legend3 = 'H3'):

    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(H1.f, H1.a, H2.f, H2.a, H3.f, H3.a)
    ax1.legend([legend1, legend2, legend3])

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(H1.f, H1.p, H2.f, H2.p, H3.f, H3.p)
    ax2.legend([legend1, legend2, legend3])

    plt.show()


def plot_transfer_function(H, legend1='H'):
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(H.f, H.a)
    axarr[0].legend([legend1])

    axarr[1].plot(H.f, H.p)
    axarr[1].legend([legend1])
    plt.show()


def plot_K1(K, legend ='K'):

    plt.plot(K[:,0], K[:,1])
    plt.legend([legend])
    plt.xlabel('K[:,0]')
    plt.ylabel('K[:,1]')
    plt.show()


def plot_2_Ks(K1, K2,  legend1='K1', legend2='K2'):

    plt.plot(K1[:, 0], K1[:, 1], K2[:, 0], K2[:, 1])
    plt.legend([legend1, legend2])

    plt.show()

def plot_3_Ks(K1, K2, K3, legend1='K1', legend2='K2', legend3='K3'):

    plt.plot(K1[:, 0], K1[:, 1], K2[:, 0], K2[:, 1], K3[:, 0], K3[:, 1])
    plt.legend([legend1, legend2, legend3])

    plt.show()
