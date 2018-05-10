function [ a, K ] = Param_Signal_pol3( u_in, in_pp, u_out, N, H_kompl)
%Unterschied zu Param_Signal2:
%Bestimmt zwei verschiedene Polynome, eines f�r den positiven und eines f�r
%den negativen Ast der Kennlinie
%Beschreibung Param_Signal2:
%Errechnet eine Parametrisierung der nichtlinearen Kennlinie des Systems in
%Form eines Potenzreihenansatzes der Ordnung N. a_i sind die Koeffizienten der
%Potenzreihe. Dabei wird das Ausgangssignal (u_out) �ber eine
%�bertragungsfunktion auf das Eingangssignal zur�ck gerechnet und dann
%anhand eines LS-Ansatzes durch Vergleich mit dem Eingangssignal u_in die
%Kennlinie bestimmt.
%u_in: eine Periode des Eingangssignals (z.B. aus .arb-Files des AWGs) -->
%muss vorher normiert werden!
%u_out: das gemessene Ausgangsignal
%N: Die Ordnung der Kennlinie (Potenzreihe)
%in_pp: Amplitude der Eingangsspannung in mVpp
% H: Komplexe �Bertragungsfunktion [f,H]
%--> Da das Eingangssignal nicht normiert ist,
%--> Achtung: manchmal ist u_outmess=-u_out -> Signal invertieren!
%--> auf U_rep=900kHz normiert

%abfangen, wenn u_in oder u_out eine Zeitspalte haben
if min(size(u_in))==2
    %Eine Periodenl�nge herausfiltern (normiert auf 900 kHz
    %Wiederholfrequenz
    %dt=u_in(2,1)-u_in(1,1);
    %L_T=round(1/900000/dt);
    u_in=u_in(:,2);
end
if min(size(u_out))==2
    %Eine Periodenl�nge herausfiltern (normiert auf 900 kHz
    %Wiederholfrequenz
    dt=u_out(2,1)-u_out(1,1);
    L_T=round(1/900000/dt);
    u_out=u_out(1:L_T,2); 
end

%Eingangssignal aus Ausgangssignal berechnen:
u_out=U_inp3(u_out, 900000, H_kompl);

l_in=length(u_in);
l_out=length(u_out);
%Signale �bereinanderlegen --> Interpolation und Signale �bereinander
%legen: 
%Interpolation
x_in=linspace(1,l_out,l_in);
x_out=linspace(1,l_out, l_out);
u_in=interp1(x_in, u_in, x_out);
%Signale �bereinanderschieben -> �ber Kreuzkorrelation
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
%%�bereinanderlegen (Maxima als Start)
%in=zeros(l_out,1);
%out=in;
%in(1:l_out-i_in)=u_in(i_in+1:l_out);
%in(l_out-i_in+1:l_out)=u_in(1:i_in);
%out(1:l_out-i_out)=u_out(i_out+1:l_out);
%out(l_out-i_out+1:l_out)=u_out(1:i_out);

%NOrmierung: u_out wird in V gemessen--> mV; u_in aus arb-file:Normierung
%h�ndisch anhand in_pp
out=1000*out;
in=in_pp/(max(in)-min(in))*in;

%Signale mit nur positiven und negativen Spannungen bestimmen
u_out_pos=out;
u_out_neg=out;
u_in_neg=in;
u_in_pos=in;

l_in=length(in);
l_out=length(out);

for ind=1:l_in
    if in(ind)<0
        u_in_pos(ind)=0;
    else
        u_in_neg(ind)=0;
    end
end
for ind=1:l_out
    if out(ind)<0
        u_out_pos(ind)=0;
    else
        u_out_neg(ind)=0;
    end
end
%u_out_full=u_out;
%u_in_full=u_in;

%Spannungsmatrix erzeugen
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%positive H�lfte%%%%%%%%%%%%%%%%%
U=zeros(l_out,N);
for ind=1:N
    U(:,ind)=u_in_pos.^ind;
end
    
a_pos=U\u_out_pos';

K_pos=K1(a_pos,1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%negative H�lfte%%%%%%%%%%%%%%%%%%%
U=zeros(l_out,N);
for ind=1:N
    U(:,ind)=u_in_neg.^ind;
end
    
a_neg=U\u_out_neg';

K_neg=K1(a_neg,1);

%%
%Kennlinie zusammensetzen
K=K_pos;
K(1:300,2)=K_neg(1:300,2);
a=zeros(N,2);
a(:,1)=a_neg;
a(:,2)=a_pos;

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

figure
plot(t,u_in_pos,t,u_out_pos)
title('Spannung positiv')
xlabel('t in us')
ylabel('u in mV')
legend('U_in', 'H^-1*U_out')

figure
plot(t,u_in_neg,t,u_out_neg)
title('Spannung negativ')
xlabel('t in us')
ylabel('u in mV')
legend('U_in', 'H^-1*U_out')
end

