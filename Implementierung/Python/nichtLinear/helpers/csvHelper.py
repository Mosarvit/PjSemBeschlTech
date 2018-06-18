import csv

def save_2cols(filename, col1, col2):

    """

    save_2cols speichert zwei vektoren gleicher Länge als CSV ab

    INPUT:

        filename : string; Dateipfad, wo abgespeichert werden soll
        col1: nx1 vector; erste Spalte (n - länge des Vektors)
        col2 : nx1 vector; zweite Spalte (n - länge des Vektors)

    OUTPUT:

        (no output)

    """

    with open(filename, 'w+', newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0, col1.shape[0]):
            writer.writerow([str(col1[i]), str(col2[i])])