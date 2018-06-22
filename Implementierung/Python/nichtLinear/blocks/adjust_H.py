def adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H):
    """
    adjust_H optimiert die Übertragungsfunktion H

    INPUT:

        Halt - nx3 array; die alte Übertragungsfunktion (n - Anzahl der Frequenzen)
            Halt[:,0] - Frequenz f
            Halt[:,1] - Amplitudenverstärkung
            Halt[:,2] - Phasenverschiebung

        Uout_ideal - nx2 array; U_? (n - Länge des Signals)
            Uout_ideal[:,0] - Zeitvektor
            Uout_ideal[:,1] - Signalvektor

        Uout_measured - nx2 array; (n - Länge des Signals)
            Uout_measured[:,0] - Zeitvektor
            Uout_measured[:,1] - Signalvektor

        sigma_H - skalar; die Schrittweite

    OUTPUT:

        Heu - nx3 array; Übertragungsfunktion (n - Anzahl der Frequenzen)
            Heu[:,0] - Frequenz f
            Heu[:,1] - Amplitudenverstärkung
            Heu[:,2] - Phasenverschiebung

    """
    Hneu = Halt
    return(Hneu)