# PjSemBeschlTech - Handhabung der Geräte

Benutzte Geräte:
	- AWG<\br> 		Keysight 33600A
	- Oszi<\br>		Tektronix TDS 5054 DOS
	- Verstärker<\br>	
	- Kavität		

## Verkabeln & Einstellen der Geräte ---- Stand 31.05.

###Vorbemerkungen:
Grundeinstellung AWG: Kanäle 1 & 2 über Tracking gleich stellen
PC: - Beachte Fire-Wall / IP-Erlaubnis gemäß Anleitung Denys (Appendix 8.1.1)
	- Treiber für Keysight laden:
		!!! Bei Erstellen des Dokuments noch nicht auf richtiges Funktionieren geprüft!
		-- IviSharedComponents (nicht: .NET) in der entsprechenden Version, 2.4.2 oder höher unter 
			http://www.ivifoundation.org/shared_components/Default.aspx
		-- 335XX / 336XX Function / Arbitrary Waveform Generator IVI and MATLAB Instrument Drivers unter:
			https://www.keysight.com/main/software.jspx?ckey=1937336&lc=ger&cc=DE&nid=-11143.0.00&id=1937336
		
		
###Getting started:
	1) Lan-Kabel hinten an Oszi, anderes Ende an den Switch, diesen mit zweitem Lan-Kabel an Computer
	2) USB-Kabel hinten an AWG, anders Ende an den PC
	3) Anschlüsse der Kavität auf Kanäle 3 & 4 des Oszi anschließen:
		- mit 50 Ohm Abschlussstück am T-Stück ans Oszi versehen
		- Oszi auf hochohmige Eingänge stellen (da 50 Ohm Abschluss des Kabels bereits durch Abschlussstück realisiert -> schützt das Oszi vor höheren Strömen)
	4) Anschluss des einen Ausgangs des AWG auf Kanal 1 des Oszi, Vorgehen analog zu 2)
	5) Anschluss & Anschalten Verstärker:
		- zweiten Ausgang des AWG auf den Eingang des Verstärkers an der Rückseite
		- Main-Schalter auf der Rückseite anstellen
		- auf der Vorderseite anschalten
		- Gain auf 100 % hoch drehen -> beste Linearität
		- Local on, RF on
	6) Beachte bei erstem Einstellen des Oszis:
		- Oszi darf nicht ans Netz des Labors, da Windows-Version zu alt, nicht mehr gesichert
		- in Windows-Oberfläche -> über roten Kreis unten rechts starten des Servers VXI-11
		- vertikale Einstellungen so regeln, dass die Signale oben / unten nicht abgeschnitten werden
	7) Ausschalten des Verstärkers:
	 -------- Jens fragen ------------


#### Was ist das Ziel der Software, wann hat sie ihren Zweck erfüllt?
 
Die Software soll fongendes können:

  1. Für ein gewünschtes Barrier-Bucket Signal U_out ein Eingangssignal U_in berechnet.
  2. Das berechnete Eingangssingal an das System senden. 
  
Nun gehen wir auf die 2 Funktionalitäten ein:


### 1. Für ein gewünschtes Signal U_out ein Eingangssignal U_in berechnen.

#### 1.1. Was wird das gewünschte Signal definiert?
 
Das gewünschte Signal kann jedes beliebige Signal sein. (Für dieses Projekt wird ein Barrier-Bucket Signal gewüscht, für die Software mach es aber keinen Unterschiede, denn sie kann mit jedem Signal arbeiten.)
    
#### 1.2. Wie wird Uin berechnet?

Das Signal Uin läuft im System folgende Stufen durch:
                                           
  Uin ----> Nichtlineares Verstärkung(a) --->-- Uquest ----> Linear Verstärkung (H) ------> Uout
  
  - das nichtliare Verstärkung wird durch eine Summe mehrerer Funktionen mit den Vorfaktoren a beschrieben
  - die lineare Verstärkung wird mit der Übertragungsfunktion H beschrieben    
   
Somit kann durch Rückrechnung für jedes beliebiege U_out das U_in bestimmt werden:

Uin <---- **get_Uin(** Uquest, a **)** <---- Uquest ---<-- **compute_Uquest(** Uout, H **)** <----- Uout

Wenn wir also die Lookup-Tabelle K und die Übertragunsfunktion H hätten, 
könnten wir U_in mithilfe der Funktionnen **Uquest** und **get_Uin** bestimmmen. 


## Ausführen der Software

Hier wird auf den Status aller zu erstellenden Funktionen eingegagen.

## Bekannte Fehlerquellen & Lösungen

	- Treiber für 