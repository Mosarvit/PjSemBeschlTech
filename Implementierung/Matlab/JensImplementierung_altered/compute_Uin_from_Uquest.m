function [ Uin ] = compute_Uin_from_Uquest( Uquest, K)


% function [ U_vv ] = Vorverzerrung2arbarb_K( inputfilename, KL, amplitude,
% f, fName )
% Erzeugt aus einem linear vorverzerrten Signal (als .arb Datei unter
% dem Pfad "inputfilename" abgelegt) ein f�r eine bestimmte Amplitude
% amplitude f�r die Kennlinie KL vor verzerrtes Signal.
% inputfilname: Dateiname des linear vorverzerrten Signal (.arb-file)
% KL: Kennlinie, Nx2 Matrix mit Eingangsspannungswerten in der ersten und
% Ausgangsspannugnswerten inder zweiten Spalte.
% amplitude: gew�nschte Amplitude des nichtlinear vorverzerrten Signals in
% mVpp.
% fName: Dateiname (samt Ordnerpfad) f�r das erzeugte nichtlinear
% vorverzerrte .arb-file
%f = Wiederholfrequenz der BB-Pulse in Hz

approach = 2 ;

if approach == 1

U = Uquest;

% K = KL;

%Steigung in linearem Bereich bestimmen
[N,i]=size(K);
%5% der Kennlinie f�r Fit der Steigung
l=0.2; % vorher 0.05
%Runden
n=round(N*l);

%Linearisierung um 0
ind1=find(K(:,2)>=0,1);  %Index, an der Kennlinie durch 0 geht
x=K(ind1:(ind1+n),1);   %n Punkte von da an f�r die Linearisierungsgerade verwenden
y=K(ind1:(ind1+n),2);
m=(sum(y.*x))/(sum(x.^2)); %Steigung

%-------> Falls U_steuer_max*m>U_Kmax: Fehler werfen oder Steigung
%bestimmen zu U_Kmax/U_steuer(U_kmax) -> damit weiterrechnen -->
%Vorverzerrung bei kleinen Amplituden = D�mpfung / Steuerspannung wird
%soweit reduziert, bis maximale Ausgangsspannung mit gegebener Kennlinie
%m�glich ist! -> Meldung ausgeben (Weiter verzerren / Abbrechen) und mit
%modifiziertem m weiter rechnen
if m*max(U(:,2))> max(K(:,2))      %Falls �ber die Kennlinie verzerrt w�rde: Linearisierungsgerade anpassen
    m=max(K(:,2))/max(U(:,2));
end
if m*min(U(:,2))< min(K(:,2))       %auch im negativen Bereich
    m=min(K(:,2))/min(U(:,2));
end

%Puffer
m=m*0.999;

%Kennlinie mit kubischen Splines fitten (Smoothing Parameter=1)
U_Steuer=linspace(round(min(K(:,1))),round(max(K(:,1))),(round(max(K(:,1)))-round(min(K(:,1))))*1000+1); %paarweise U_Steuer-U_out in 0,001V Schritten
%KL=csaps(K(:,1),K(:,2),1,U_Steuer);
KL=spline(K(:,1),K(:,2),U_Steuer);
Kennlinie=[U_Steuer', KL'];  
U_vv=U;

%nichtlineare Vorverzerrung an der Kennlinie
for ind=1:size(U(:,1))
    U_a=m*U(ind,2);%gew�nschte Ausgangsspannung=Ui*m
    l=find(Kennlinie(:,2)>=U_a,1);%in Kennlinie suchen -> Index l (Stelle, an der der Wert der Ausgangsspannung die gew�nschte Spannung �bersteigt)
    U_vv(ind,2)=Kennlinie(l,1); %dem Zeitschritt die passende Steuerspannung zuordnen
end

Uin = U_vv;


elseif approach == 2
 
Uin(:,1) = Uquest(:,1);
[~, index] = sort(K(:,1));
Uin(:,2) = interp1(K(index,2), K(index,1), Uquest(:,2));

end

end

