# PjSemBeschlTech


## Einfache Erklärung des Codes Software

Hier soll die Software sehr allgemein und in möglichst einfacher Sprache erklärt werden. Ganz nach dem Motto :
"Wenn du es einem Sechjärigen nicht erklären kannst, hast du es nicht verstanden." (angeblich ein Zitat von A.Einstein)
Dieser Teil ist wichtig, damit wir uns auf der oberen Design-Ebene maximal einig sind, was die Software macht.
Es werden bewusst soweit es geht die Details der Implementierung ausgelassen. 
Ziel ist es, zu beschreiben, was die wichtigsten Funktionen machen und nicht Wie sie es machen. 
Für die Erklärung des Wie kann auf das Skript oder den Sourcecode zugegriffen werden. 

Hinweis: Die Ein- und Ausgabegabevariablen der Funktionen sind in dieser Erklärung als Pseudocode zu betrachten 
(stimmen also teilweise nicht mit dem echten Code überein). Die detailierte Beschreibungen der Fuktionen und deren Parameter 
werden in den Funktionen selbst dokumentiert.

Hier kommt also der Versuch einer einfachen Erklärung (für einen Sechjährigen):



 - Was ist das Ziel der Software, wann hat sie ihren Zweck erfüllt?
 
Die Software soll fongendes können:

  1. Für ein gewünschtes Barrier-Bucket Signal U_out ein Eingangssignal U_in berechnet.
  2. Das berechnete Eingangssingal an das System senden. 
  
Nun gehen wir auf die 2 Funktionalitäten ein:


### 1. Für ein gewünschtes Barrier-Bucket Signal U_out ein Eingangssignal U_in berechnen.

#### 1.1. Wodurch wird das gewünschte Barrier-Bucket Signal definiert?
 
Das gewünschte Barrier-Bucket Signal wird definiert durch: 

  - die Wiederholfrequenz f_rep
  - die Barrier_Bucket Frequenz f_bb
  - die Grenzfrequenz f_g   

    
#### 1.2. Wie wird U_in berechnet?

Das Signal U_in läuft im System folgende Stufen durch:
                                           
  U_in ----> Nichtlineares Verstärkung(a) --->-- U_quest ----> Linear Verstärkung (H) ------> U_out
  
  - das nichtliare Verstärkung wird durch eine Summe mehrerer Funktionen mit den Vorfaktoren a beschrieben
  - die lineare Verstärkung wird mit der Übertragungsfunktion H beschrieben    
   
Somit kann durch Rückrechnung für jedes beliebiege U_out das U_in bestimmt werden:

U_in <---- getU_in(U_quest, a) <---- U_quest ---<-- getU_quest(U_out, H) ------ U_out

Wenn wir also die Vorfaktoren a und die Übertragunsfunktion H hätten, 
könnten wir U_in mithilfe der Funktionnen U_quest und getU_in bestimmmen. 

#### 1.3. Wie kann die Übertragungsfunktion H bestimmt werden?
 
 Für die Bestimmung von H gibt es bereits einen funktionierenen Python Code (von Denys).
 Dabei wird für niedrigen Amplituden die gesamte Verstärkung als linear angenommen und das System vereinfacht sich zu:
 
   U_in ----> Linear Verstärkung (H) ------> U_out

Um H zu bestimmen, wird die zur Verfügung gestellte funktionierende Funktion getH benutzt. 
getH kommuniziert mit den Geräten und gibt das komplexe H aus. 

!! Zu klären: bei dem nichtlinearen System wird die die lineare Verstärkung separat betrachtet. Eignet sich getH immer noch dazu, das H zu bestimmen?

#### 1.4. Wie können die Vorfaktoren a bestimmt werden?
 
Wir betrachten wieder das vollständige nichtlineare System:

U_in <---- getU_in(U_quest, a) <---- U_quest ---<-- getU_quest(U_out, H) ------ U_out

Wir senden ein beliebiges Signal U_in und messen U_out. Wir nehmen an, dass die Übertragungsfunktion H bestimmt wurde. 
Somit können mir mithilfe von getU_quest das getU_quest bestimmen. 

Nun können mit der Funktion geta(U_quest, U_in) die Vorfaktoren a bestimmt werden


### 2. Das berechnete Eingangssingal an das System senden. 

#### 2.1. Wie wird das berechnete Signal an das System gesendet?
 - Das Senden des berechneten Signals U_in wird von der Funktion sendToAWG(U_in) ausgeführt.

## Status der Codes

Hier wird auf den Status aller zu erstellenden Funktionen eingegagen.

## Zeitplanung:

#### 11.05. 11:00 - Treffen an der TU

Zielsetzung: 
 - Die Unterlagen besprechen und den weiteren Verlauf planen

Status: Findet statt

#### 18.05. 11:00 - Termin mit Jen

Zielsetzung: 
  - Sich die Geräte erklären lassen  
  - Den Linearen Code von Denys ausprobieren
  - evtl. unseren Code ausporobieren (falls dieser bis dahin läuft)
  
Status: Noch nicht angefragt

## Frei Kommentare

#### 05.08. Artem : 

Hab nun diesen ersten Readme erstellt. Es hat erstmal nur die drei Abschnitte: 
  - Einfache Beschreibung des Codes Software
  - Status des Codes
  - Zeitplanung
  
  Zu dem Status des Codes werde ich an einem anderen Tag etwas schreiben. 
  Falls es Ideen für weiter Abschnitte gibt, oder auch andere Anregungen, sagt bitte Bescheid. 
  Gegenseiteig Kritik ist sehr wichtig bei so einem Projekt. 

