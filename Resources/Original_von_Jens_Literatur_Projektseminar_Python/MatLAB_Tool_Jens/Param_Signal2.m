function [ a, K ] = Param_Signal2( u_in, in_pp, u_out, N, H_kompl)
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
u_out=U_inp3(u_out, 900000, H_kompl);

l_in=length(u_in);
l_out=length(u_out);
%Signale übereinanderlegen --> Interpolation und Signale übereinander
%legen: 
%Interpolation
x_in=linspace(1,l_out,l_in);
x_out=linspace(1,l_out, l_out);
u_in=interp1(x_in, u_in, x_out);
%Signale übereinanderschieben -> über Kreuzkorrelation
xc=xcorr(u_in, u_out);
shift=find(xc==max(xc));

%if shift>=0
%   in=u_in;
%   out=in;
%   out(1:l_out-shift)=u_out(shift+1:end);
%   out(l_out-shift+1:end)=u_out(1:shift);
%end

%if shift>=0
%   out=u_out;
%   in=out;
%   in(1:l_out-shift)=u_in(shift+1:end);
%   in(l_out-shift+1:end)=u_in(1:shift);
%end


if shift > length(u_out)
    shift=length(u_out)-shift;
end

if shift>=0
   out=u_out;
   in=out;
   in(1:l_out-shift)=u_in(shift+1:end);
   in(l_out-shift+1:end)=u_in(1:shift);
end

if shift<0
   out=u_out;
   in=out;
   in(l_out+shift+1:end)=u_in(1:-shift);
   in(1:l_out+shift)=u_in(-shift+1:end);
end


%i_in=find(u_in==max(u_in));
%i_out=find(u_out==max(u_out));
%%Übereinanderlegen (Maxima als Start)
%in=zeros(l_out,1);
%out=in;
%in(1:l_out-i_in)=u_in(i_in+1:l_out);
%in(l_out-i_in+1:l_out)=u_in(1:i_in);
%out(1:l_out-i_out)=u_out(i_out+1:l_out);
%out(l_out-i_out+1:l_out)=u_out(1:i_out);

%NOrmierung: u_out wird in V gemessen--> mV; u_in aus arb-file:Normierung
%händisch anhand in_pp
out=1000*out;
in=in_pp/(max(in)-min(in))*in;

%Spannungsmatrix erzeugen
U=zeros(l_out,N);
for ind=1:N
    U(:,ind)=in.^ind;
end
    
a=U\out';

K=K1(a,1);

figure
t=linspace(0,1/900000*1000000,length(in));
plot(t,in,t,out)
title('Spannungssignale')
xlabel('t in us')
ylabel('u in mV')
legend('U_in', 'H^-1*U_out')

figure
plot(K(:,1),K(:,2));
title('Kennlinie')
xlabel('U_in in mV')
ylabel('U_out in mV')

end

