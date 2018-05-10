function [ a, K ] = Param_Signal2( u_in, in_pp, u_out, N, H_kompl, verbosity)
%Unterschied zu Param_Signal2:
%Bestimmt zwei verschiedene Polynome, eines für den positiven und eines für
%den negativen Ast der Kennlinie
%Beschreibung Param_Signal2:
%Errechnet eine Parametrisierung der nichtlinearen Kennlinie des Systems in
%Form eines Potenzreihenansatzes der Ordnung N. a_i sind die Koeffizienten der
%Potenzreihe. Dabei wird das Ausgangssignal (u_out) über eine
%Übertragungsfunktion auf das Eingangssignal zurück gerechnet und dann
%anhand eines LS-Ansatzes durch Vergleich mit dem Eingangssignal u_in die
%Kennlinie bestimmt.
%u_in: eine Periode des Eingangssignals (z.B. aus .arb-Files des AWGs) -->
%muss vorher normiert werden!
%u_out: das gemessene Ausgangsignal
%N: Die Ordnung der Kennlinie (Potenzreihe)
%in_pp: Amplitude der Eingangsspannung in mVpp
% H: Komplexe ÜBertragungsfunktion [f,H]
%--> Da das Eingangssignal nicht normiert ist,
%--> Achtung: manchmal ist u_outmess=-u_out -> Signal invertieren!
%--> auf U_rep=900kHz normiert

%abfangen, wenn u_in oder u_out eine Zeitspalte haben
if min(size(u_in))==2
    %Eine Periodenlänge herausfiltern (normiert auf 900 kHz
    %Wiederholfrequenz
    %dt=u_in(2,1)-u_in(1,1);
    %L_T=round(1/900000/dt);
    u_in=u_in(:,2);
end
if min(size(u_out))==2
    %Eine Periodenlänge herausfiltern (normiert auf 900 kHz
    %Wiederholfrequenz
    dt=u_out(2,1)-u_out(1,1);
    L_T=round(1/900000/dt);
    u_out=u_out(1:L_T,2); 
end

%Eingangssignal aus Ausgangssignal berechnen:
u_out=getU_quest(u_out, 900000, H_kompl, verbosity);

[ a, K ] = geta( u_in, in_pp, u_out, N, verbosity);



end

