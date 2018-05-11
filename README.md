# PjSemBeschlTech


## Einfache Erklärung der Software

Hier soll die Software sehr allgemein und in möglichst einfacher Sprache erklärt werden. Ganz nach dem Motto :
"Wenn du es einem Sechjärigen nicht erklären kannst, hast du es nicht verstanden." (angeblich ein Zitat von A.Einstein)
Dieser Teil ist wichtig, damit wir uns auf der oberen Design-Ebene maximal einig sind, was die Software macht.
Es werden bewusst soweit es geht die Details der Implementierung sowie Fachwörter ausgelassen. 
Ziel ist es, zu beschreiben, Was die wichtigsten Funktionen machen und nicht Wie sie es machen. 
Für die Erklärung des Wie kann auf das Skript oder den Sourcecode zugegriffen werden. 

*Hinweis:* Die Ein- und Ausgabegabevariablen der Funktionen sind in dieser Erklärung als Pseudocode zu betrachten 
(stimmen also teilweise nicht mit dem echten Code überein). Die detailierte Beschreibungen der Fuktionen und deren Parameter 
werden in den Funktionen selbst dokumentiert.

Hier kommt also der Versuch einer einfachen Erklärung (für einen Sechjährigen):



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

Wenn wir also die Vorfaktoren a und die Übertragunsfunktion H hätten, 
könnten wir U_in mithilfe der Funktionnen **Uquest** und **get_Uin** bestimmmen. 

#### 1.3. Wie kann die Übertragungsfunktion H bestimmt werden?
 
 Für die Bestimmung von H gibt es bereits einen funktionierenen Python Code (von Denys).
 Dabei wird für niedrigen Amplituden die gesamte Verstärkung als linear angenommen und das System vereinfacht sich zu:
 
   Uin ----> Linear Verstärkung (H) ------> Uout

Um H zu bestimmen, wird die zur Verfügung gestellte funktionierende Funktion getH benutzt. 
getH kommuniziert mit den Geräten und gibt das komplexe H aus. 

!! Zu klären: bei dem nichtlinearen System wird die die lineare Verstärkung separat betrachtet. Eignet sich get_H immer noch dazu, das H zu bestimmen?

#### 1.4. Wie können die Vorfaktoren a bestimmt werden?
 
Wir betrachten wieder das vollständige nichtlineare System:

Uin <---- **compute_Uin(** Uquest, K **)** <---- Uquest  ---<-- **compute_Uquest(** Uout, H **)** <----- Uout

Für ein beliebiges Uout berechnen wir zuerst U_quest0 mit **compute_Uquest** . Das U_quest0 senden wir in das System als Uin und messen das  neue Uquest1 (An dieser Stelle ist es etwas verwirrend, ich weiss). Mithilfe von **get_aK(** Uquest1, Uin **)** berechnen wir a. 

### 2. Das berechnete Eingangssingal an das System senden. 

#### 2.1. Wie wird das berechnete Signal an das System gesendet?
Das Senden des berechneten Signals Uin wird von der Funktion **sendToAWG(** Uin **)** ausgeführt.

## Status der Codes

Hier wird auf den Status aller zu erstellenden Funktionen eingegagen.

## Aufgaben und Zuständigkeitsbereiche

*Anmerkung:* momentan werden hier lediglich die momentaten Aufgabenverteilungen aufgeführt. 

Kommunikation mit Jens: Artem<br/>
Reportführung nach jedem Treffen: Jonas<br/>
Zeitplanung Abschnitt verwalten: Jonas<br/>

Design des Codes: Artem<br/>
Unit & System tests: Artem<br/>
Programmieren der Funktionen: Artem<br/>
Documentation des Codes: noch nicht zugewiesen<br/>
Testen des Codes an den Geräten: noch nicht zugewiesen<br/>

Report in Latex schreiben: noch nicht zugewiesen<br/>
Präsentation erstellen: noch nicht zugewiesen<br/>

## Fragen zu klären

#### Frage:<br/>
Im Matlab-Code von Jens in U_inp3.m in Zeile 44 :
```
Y=2*ufft/L;
```
Warum wird hier mit 2 multipliziert?

#### Überlegung:<br/>
Es wird mit 2 multipliziert, weil die Impedanzen angepasst sind.

#### Antwort:<br/>
noch keine Antwort

----------------------------------------------------------------------------------------------------------------------------------------
#### Frage:<br/>
Gibt es bereits eine Implementierung von **getU_in(** U_quest, a **)** in Matlab?

#### Überlegung:<br/>
Jens Fragen.

#### Antwort:<br/>
noch keine Antwort

----------------------------------------------------------------------------------------------------------------------------------------
#### Frage:<br/>
Nehmen wir an, dass die nichlineare Verzerrung frequenzuanhängig ist?

#### Überlegung:<br/>
Jens Fragen.

#### Antwort:<br/>
noch keine Antwort

----------------------------------------------------------------------------------------------------------------------------------------

#### Frage:<br/>
Reicht es aus, a einmal zu berechnen, oder soll a jedes Mal neu berechnet werden?

#### Überlegung:<br/>
Jens Fragen.

#### Antwort:<br/>
noch keine Antwort

----------------------------------------------------------------------------------------------------------------------------------------

#### Frage:<br/>
Warum geht die K Kennlinie nur bis 300 mV

#### Überlegung:<br/>
Jens Fragen.

#### Antwort:<br/>
noch keine Antwort

----------------------------------------------------------------------------------------------------------------------------------------
#### Frage:<br/>
Sind alle Kabel / Geräte (sonstige?) am GSI vor Ort, damit wir am 18.05. die Testdaten für Matlab nochmal neu erzeugen und messen können? Ziel ist, durch senden des (bereits durch Matlab berechneten) Eingangssignals ein Ausgangssignal zu messen und auf Übereinstimmung mit den bereits gegebenen Daten zu prüfen.

#### Überlegung:<br/>
Jens Fragen.

#### Antwort:<br/>
noch keine Antwort

----------------------------------------------------------------------------------------------------------------------------------------

#### Frage:<br/>
Muss das ideale BB Signal "per Hand" Fourier-Transformiert sein, oder reicht es aus, ein ideales BB Singal zu erschaffen und es dann mit FFT zu transformieren?

#### Überlegung:<br/>
Jens Fragen.

#### Antwort:<br/>
noch keine Antwort

----------------------------------------------------------------------------------------------------------------------------------------

#### Frage:<br/>
Welche VISA-Bibliothek sollen wir nehmen?

#### Überlegung:<br/>
Jens Fragen.

#### Antwort:<br/>
noch keine Antwort

----------------------------------------------------------------------------------------------------------------------------------------

## Zeitplanung:

#### 11.05. 11:00 - Treffen an der TU

Zielsetzung: 
 - Die Unterlagen besprechen und den weiteren Verlauf planen

Status: Findet statt

#### 18.05. 11:00 - Termin mit Jen

Zielsetzung: 
  - Sich die Geräte erklären lassen  
  - Für den linearen Fall den Code von Denys ausprobieren
  - Für den nichtlinearen Fall die Funktion evaluateWithMatlabData ausprobieren
  
Status: angefragt bei Jens - Update: Findet Statt _MN

## Freie Kommentare

#### 05.08. Artem : 

Hab nun diesen ersten Readme erstellt. Es hat erstmal nur die drei Abschnitte: 
  - Einfache Beschreibung des Codes Software
  - Status des Codes
  - Zeitplanung
  
  Zu dem Status des Codes werde ich an einem anderen Tag etwas schreiben. 
  Falls es Ideen für weiter Abschnitte gibt, oder auch andere Anregungen, sagt bitte Bescheid. 
  Gegenseiteig Kritik ist sehr wichtig bei so einem Projekt. 

