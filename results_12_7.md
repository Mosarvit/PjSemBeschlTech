Testen an der GSI 12. Juli 2018
Anwesend: Artem, Jonas, Max

TODOs vorrangig
- adjust_H testen

jetzige TODOs
1. (Artem) Test für compute_Uin_from_Uquest 
  - für zu hohe Amplituden => nicht bijektives K
2. Test Daten automatisch speichern
  - Routine in getH_denys könnte vielleicht genutzt werden
  - Readme erstellen um Daten/Fehler zu beschreiben
  - Reproduktion des Fehlers sollte möglich sein
3. (Jonas) Grundfrequenz am AWG einstellen
  - läuft soweit
  - man braucht nur die erste Variante mit der Samplerate für measure_H
  - Lösung: 2 Übergabeparameter
4. (Max) Anpassung DSO
  - vertikale Anpassung der einzelnen Channel
  - horizontale Anpassung => Projektarbeit Denys/Armin
5. (Jonas) Adjust_H richtige Einstellung finden
  - zugroßes Ration Umeas/Uideal durch Nulldurchgänge der sinc Funktion
  - Rauschen?
  - cutten auf rms
  - Amplituden Spektrum sah gut aus, Phase eher weniger
  - an signal_class anpassen
6. compute a/K
  - Funktion zum Speichern/Einlesen
7. (Max) compute Uquest FFT Spektrum auf richtigen Frequenz Vektor legen (Max)
  - Vermutung?!
8. (Artem) generate_BB_signal
  - bessere Auflösung für FFT
9. (Artem) signal_class
  - FFT speichern (keine Zick Zack Phase ;) )
10. (Artem) All_tezts
  - Mock-System automatisch anpassen
11. (All) Abgabe
  - wir haben eine Frist bekommen FÜR ALLES - holy moly
