Besprechung 16.07. - Kurzprotokoll
Update: 1.8.

Termine -> siehe Gruppe

------------------ Deadlines -----------------
### bis 27.7. abschliessende Funktionalitaet im Code 

### bis 1.8. Auflistung, welche Daten wir an der GSI noch generieren muessen fuer Report / Praesentation

### bis 9.8. Praesentation und Report im vorlaufigen Endzustand an Jens schicken -> Feedback

### bis 12.8. 18 Uhr: endgueltige Version Praesentation und Report

### 13.8. 10 Uhr: grosser Showdown
### 13.8. 11 Uhr: grosses Aufatmen

------------------ Kommentare ----------------

# Fehler Berechnen von Signalen als Abweichung
	- Artem: neue Implementierung, etwa Median, Standardabweichung
		-> Güte in einfach?

# Kennlinie
	- können wir sicherstellen, dass K bijektiv im Berechnungsbereich ist?
		-> Max schaut sich Problematik an!!! Gaaanz grosses Kino!

------------------ TODOs ---------------------
# alle: 
beim Sammeln von Ideen fuer Report notieren, welche Daten an der GSI generiert werden muessen, um Aussagen zu veranschaulichen

# bis nächstes Mal an GSI zu tun:

# nächstes Mal an GSI zu tun:
	- notieren, wieviele Samples in AWG genutzt werden: 221
	- Messdaten generieren:
		- evaluate adjust_H:
			- I I zweimal ganz ohne RMS (mit sigma = 0.5) oder Promille Anpassung laufen lassen (mind. 5 Iterationen)
				zweimal, um Einfluss von Rauschen zu vergleichen
			- einmal mit sigma = 0.2 ohne alles laufen lassen (mind. 5 Iterationen), vergleich mit obigem
			- einmal nur mit Promille Anpassung (ca. 3 Prom) laufen lassen (mind. 5 Iterationen)
			- einmal nur mit RMS Anpassung laufen lassen (mehr als 5 Iterationen!)
			- einmal mit beiden Anpassungen durchlaufen lassen (ca. 5 Iterationen)
			(ideal: jeweils immer mitschreiben, wie groß der RMS wirklich ist)
		- evaluate adjust_a:
			- festes V_PP (von Anfang an f. Kennlinie schon)(mind 5 Iterationen, sigma=0.5)
			- größeres V_PP (nichtlinearen Bereich ausfahren)
			- mit sigma = 0.2 
	
	- Geraetekommunikation: 
		- evaluate_connect_devices mit neuem Versuch 2 für AWG testen und ggf. in write_to_AWG übernehmen
		- evaluate_connect_devices mit neuem Versuch 5 für AWG testen und ggf. in write_to_AWG übernehmen
			!!!! Fehler, falls auftreten, dokumentieren! Abhilfe u. U. vor Ort mit Programming tips möglich
		- sobald Zeitverhalten funktionsfähig, Laufzeiten der unterschiedliche, zeitaufwendigen Befehle einzeln dokumentieren!
		- zur Sicherheit: Test von Zeitversuch mit BUSY? am DSO! -> eher als Standard, da stabiler als OPC?
		- falls Zeit: Verbindung mit zweitem PC testen (just for fun! neues Oszi wird ja eh bald genutzt)
			
	- K kontrollieren: Bereiche für Berechnung von a checken & festhalten
		-> Problem Bijektivität in initialem K gegeben????


# Aufgaben:

## Artem:
	- (siehe Issue) eine Klasse fuer Kennlinie ``K`` erstellen, insb. Einbinden der Grenzen, in denen ``K`` berechnet wurde
	- Dokumentation für Code und Design grob erstellen für Report (bis Sa Abend)
		- warum evaluate/compute/determine .. als Namen gewählt?
		- Ordnerstruktur
		- TDD
		- Mock-System
		- (Refactoring)
		- Vorgehen bei Implementierung aus Matlab
		- Versionskontrolle, "Protokoll" Kommentare
	
## Max 
	- (siehe Issue) ``adjust_a`` und ``evaluate..`` fertig stellen fuer Test -> V_PP anpassen in K
	- Eintrag Latex ``adjust_a``
	- ggf. Anpassung der Skalierung des Oszis an abgeaenderte Methode ``generate_BB_signal``
	- Anpassen der Doku des Designs / Code
	- Wie kann man Ausgang und Eingangssignal vergleichen (mit hinsicht auf Amplitude/Vpp)
	
## Jonas
	- (siehe Issue) ``generate_BB_signal`` und Verweise anpassen an (richtige) Definition von ``f_rep``, ``sample_rate`` und ``timestep``. Ggf. auch verwandte Aufrufe/Methoden gegenchecken
	- ``runme`` und ``settings`` in Absprache mit Jens anpassen, s.d. Nutzbarkeit sichergestellt ist
	
# Aufgaben im Code fuer nach der Praesentation:
	- sicherstellen, dass ausfuehrlich kommentiert wurde 
	- sicherstellen, dass in Englisch kommentiert wurde
	- in Absprache mit Jens / anderen Nutzern des Programms die Dokumentation ueberpruefen
	- ``type_check_...`` in Methoden einbinden
	- sicherstellen, dass auf Variablen aus ``settings`` an allen notwendigen Stellen der Methoden zugegriffen wird

	
------------------ Topics Report -------------
# Gliederung analog zu Zwischenpraesentation:

## Einleitung: (Max)
	- Modell BB
	- Motivation PJSem
	- Problem-/Aufgabenstellung PJSem
	
## Bericht ueber Vorgehen:
	- Was war vorgegeben / womit wurde angefangen? (Matlab zu Python) (Max)
	- Geraetekommunikation (Jonas)
	- Optimierung: (Jonas)
		. Daten und Versuche
		. (Einbindung Tool zur Bewertung)
	- Optimierung a/K (Max)

## Evaluierung / Erkenntnisse (erste Meta-Ebene)
	- Erfuellung von Problem-/Aufgabenstellung ?
	- neue Moeglichkeiten durch die Nutzung unseres Programms
	- Allgemeine Vorteile unseres Code-Designs fuer die Nutzung in Messsituationen und Probleme
	- Bewertung Sinnhaftigkeit Optimierung
	- Erfahrung Problematik FFT-Berechnung-> ein Zeitschritt zu wenig für Berechnung Periodendauer!
	- Problematisch: wenig RF-Tool einbindung (Bewertung, Erzeugung Singlesine)
	

	