def adjust_a(aalt, Uout_ideal, Uout_measured, sigma_a):
    """
    adjust_a optimiert die Vorfaktoren a

    INPUT:

        aalt - Nx1 vector; die Vorfaktoren; (N - Polynomgrad der Approximierugnsmatrix)

        Uout_ideal - nx2 array; U_? (n - Länge des Signals)
            Uout_ideal[:,0] - Zeitvektor
            Uout_ideal[:,1] - Signalvektor

        Uout_measured - nx2 array; (n - Länge des Signals)
            Uout_measured[:,0] - Zeitvektor
            Uout_measured[:,1] - Signalvektor

        sigma_a - skalar; die Schrittweite

    OUTPUT:

        aneu - Nx1 vector; die Vorfaktoren; (N - Polynomgrad der Approximierugnsmatrix)

    """
    aneu = aalt
    return(aneu)