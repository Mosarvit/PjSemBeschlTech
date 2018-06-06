# PjSemBeschlTech - Handhabung der Geräte

Benutzte Geräte:
- AWG		Keysight 33600A
- Oszi		Tektronix TDS 5054 DOS
- Verstärker	
- Kavität		

## Verkabeln & Einstellen der Geräte ---- Stand 31.05.

###Vorbemerkungen:
Grundeinstellung AWG: Kanäle 1 & 2 über Tracking gleich stellen

PC: 
- Beachte Fire-Wall / IP-Erlaubnis gemäß Anleitung Denys (Appendix 8.1.1)
	- NI-Visa installieren siehe Website (z.B. unter dem [link](http://search.ni.com/nisearch/app/main/p/bot/no/ap/tech/lang/de/pg/1/sn/ssnav:drv/q/ni%20visa%20/) )
	- Treiber für Keysight laden:
		!!! Bei Erstellen des Dokuments noch nicht auf richtiges Funktionieren geprüft!
		-- IviSharedComponents (nicht: .NET) in der entsprechenden Version, 2.4.2 oder höher unter 
			http://www.ivifoundation.org/shared_components/Default.aspx
		-- 335XX / 336XX Function / Arbitrary Waveform Generator IVI and MATLAB Instrument Drivers unter:
			https://www.keysight.com/main/software.jspx?ckey=1937336&lc=ger&cc=DE&nid=-11143.0.00&id=1937336
	- PyVISA in Python installieren, z.B. Version 1.9.0
		
		
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
	- Oszi darf nicht mit Internet des Labors verbunden werden, da Windows-Version zu alt, nicht mehr gesichert
	- in Windows-Oberfläche -> über roten Kreis unten rechts starten des Servers VXI-11
	- vertikale Einstellungen so regeln, dass die Signale oben / unten nicht abgeschnitten werden
7) Ausschalten des Verstärkers:
	 -------- Jens fragen ------------


## Bekannte Fehlerquellen & Lösungen
- Treiber nicht installiert -> siehe oben
