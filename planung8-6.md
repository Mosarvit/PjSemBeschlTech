
heute:

- Measure-Fkt testen
- funktionieren die Treiber? Auch für das Oszi?
- Fragen Readme


- nächste Steps klären
	- Optimierung Algorithmus: Iterative Anpassung von Kennlinie und Übertragungsfunktion
	- Zeitverhalten VISA-Anweisung optimieren
	
	
TODO:
- Check auf Amplitude: max. AWG Vpp auf 1 V setzen! Sonst Zerstörung des Verstärkers! 
	(muesste ja auch ausreichen, Vpp_max ist mit 0.6 V hoechstens moeglich nach Kennlinie
- Visa Fehler Vi_Error_System_Error (-1073807360) unknown system error (miscellaneous error)
- warum uquest als komplex in Python -> Im << Re (Im ~10^-16)
	-> Vermutung: Rechengenauigkeit sorgt dafür, dass die Im-Teile sich nicht genau zu 0 addieren
	-> Vermutung 2: Python arbeitet mit anderen Indizes und Darstellung der FFT, dadurch ergeben sich andere Verschiebungen, die nicht richtig berücksichtigt wurden
	
	Lösung 1: Realteil der berechneten komplexen Faktoren c bilden
	Lösung 2: Dokumentation der FFT durchlesen und Code anpassen

Erfahrung: Bei Visa-Fehlern erstmal alle Geräte neu starten!
! in Dokumentation: Welche Datenformate (z. B. Spalte 0 Zeit, Spalte 1 Spannung) werden verwendet?

Artem: Schnittstelle Optimierung, Einbindung getH anpassen, H speichern bei evaluate -> nicht in jedem Durchlauf neu berechnen
Max: Optimierung nichtlineare Übertragung
Jonas: Optimierung lineare Übertragung, Visa-Zeitverhalten?

usb klappt 
dso -> wie ansteuern?

