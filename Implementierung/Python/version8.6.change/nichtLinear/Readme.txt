========================================================================================================================
Ordner
========================================================================================================================

copmpute:

 - Beinhaltet alle compute_ - Funktionen. Was compute bedeutet siehe Konventionen

------------------------------------------------------------------------------------------------------------------------

data:

 - Daten, die während der Laufzeit gespeichert wurden.
 - Testdaten.

------------------------------------------------------------------------------------------------------------------------

evaluation:

 - Alle Funktionen, die zur Evaluierung. Was evaluation bedeutet siehe Konventionen

------------------------------------------------------------------------------------------------------------------------

helpers:

 - Alle Funktionen, die von mehreren anderen Funktionen genutzt werden.

------------------------------------------------------------------------------------------------------------------------

later:

 - Funktionen, die später evtl. geschrieben werden sollten.

------------------------------------------------------------------------------------------------------------------------

test:

 - unit tests
 - system tests

------------------------------------------------------------------------------------------------------------------------

venv:

 - Projekt-Enviroment

------------------------------------------------------------------------------------------------------------------------

========================================================================================================================
Konventionen
========================================================================================================================

compute vs. get:

 - sind beides präfixe von Funktionsnamen
 - eine copmpute-Funktion erhält Daten und verarbeitet diese, entspricht der Funktionalität wie in einem Blockdiagramm des Systems.
get
 - eine get-Funktion kommuniziert mit den Geräten und benutzt compute-Funktion(en), um die gewünschte Daten zu erzeugen.
 Im Idealfall soll für alle get-Funktionen folgendes gelten: man lässt getK laufen und erhält K als output, vorausgesetzt
 die Geräte sind korrekt angeschlossen.