Besprechung 16.07. - Kurzprotokoll

Termine -> siehe Gruppe

------------------ Deadlines -----------------
### bis 27.7. abschliessende Funktionalitaet im Code 

### bis 1.8. Auflistung, welche Daten wir an der GSI noch generieren muessen fuer Report / Praesentation

### bis 9.8. Praesentation und Report im vorlaufigen Endzustand an Jens schicken -> Feedback

### bis 12.8. 18 Uhr: endgueltige Version Praesentation und Report

### 13.8. 10 Uhr: grosser Showdown
### 13.8. 11 Uhr: grosses Aufatmen

------------------ TODOs ---------------------
# alle: 
beim Sammeln von Ideen fuer Report notieren, welche Daten an der GSI generiert werden muessen, um Aussagen zu veranschaulichen

# Aufgaben im Code:

## Artem:
	- (siehe Issue) eine Klasse fuer Kennlinie ``K`` erstellen, insb. Einbinden der Grenzen, in denen ``K`` berechnet wurde
	- (siehe Issue) Mock-System ausbauen und freundlich fuer weitere Anwender gestalten

## Max 
	- (siehe Issue) speichern von Messdaten eines Programm-Durchlaufs in eigenen Ordner 
	- (siehe Issue) ``adjust_a`` und ``evaluate..`` fertig stellen fuer Test am Freitag
	- ggf. Anpassung der Skalierung des Oszis an abgeaenderte Methode ``generate_BB_signal``

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
	- Aufraeumen von Code: (Infos von Artem)(Max)
		. Motivation fuer Code-Design und warum ausgewaehlt fuer Setting einer Messsituation
		. Refactoring
		. TDD implementieren
		. Klassen und ``helpers``-System
		. (Mock-System)
	- Geraetekommunikation (Jonas)
	- Dokumentation, Konventionen, Konzept hinter Konvention und Dokumentation (Jonas)
	- Optimierung: (Jonas)
		. Idee
		. Implementierung
		. Daten und Versuche
		. (Einbindung Tool zur Bewertung)
		. (ggf. Problematik mit Samplerate des AWG)
	- Optimierung a/K (Max)

## Evaluierung / Erkenntnisse (erste Meta-Ebene)
	- Erfuellung von Problem-/Aufgabenstellung ?
	- neue Moeglichkeiten durch die Nutzung unseres Programms
	- Allgemeine Vorteile unseres Code-Designs fuer die Nutzung in Messsituationen und Probleme
	- Bewertung Sinnhaftigkeit Optimierung
	
## Ausblick / weitere Ideen:
	- RF-Tools, Kommandozeilen-Ausfuehrung
	- Optimierung:
		- alternierende / parallele Iteration?
		- Formel sinnvoll?
		- Rauschen filtern?
		- Interpolationsfehler bei Nulldurchgaengen des Spektrums reduzieren?
	