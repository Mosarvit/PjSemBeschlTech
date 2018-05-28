function [ Uin ] = compute_Uin_from_Uquest( Uquest, K, amplitude )
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


%Unterschied zu Vorverzerrung2arbarb:


%Einlesen des Eingangssignals

% csv = findstr(inputfilename, '.csv');
% xlsx = findstr(inputfilename, '.xlsx');
% pattern = '[0-9]+.[0-9]+(e)?(+)?(-)?([0-9]+)?';

% %.csv
% if csv > 0
%     U = csvread(inputfilename);
% %.xls
% else if xlsx > 0
%         uiwait(msgbox('Zeitschritte Linear Vorverzerrtes Eingangssignal ausw�hlen','Select Zeitschritte','modal'));
%         U1 = xlsread(inputfilename, -1);
%         uiwait(msgbox('Spannungen Linear Vorverzerrtes Eingangssignal ausw�hlen','Select Spannungen','modal'));
%         U2 = xlsread(inputfilename, -1);
%         U = [U1, U2];
% %.arb
%     else
%         fid = fopen(inputfilename, 'r');
%         fileformat = fgetl(fid);
%         channelcount = fgetl(fid);
%         columnchar = fgetl(fid);
%         samplerate = fgetl(fid);
%         highlevel = fgetl(fid);
%         lowlevel = fgetl(fid);
%         datatype = fgetl(fid);
%         filter= fgetl(fid);
%         datapoints = fgetl(fid);
%         datastring = fgetl(fid);
%         
%         formatSpec = '%i';
%         rawdata = fscanf(fid, formatSpec);
%         fclose(fid);
% 
%         highlevel = str2num(char(regexp(highlevel,pattern,'match')));
%         lowlevel = str2num(char(regexp(lowlevel,pattern,'match')));
%         datapoints = str2num(char(regexp(datapoints,pattern,'match')));
%         samplerate = str2num(char(regexp(samplerate,pattern,'match')));
% 
%         rawdata = rawdata./32767;
%         rawdata = rawdata.*max(abs(highlevel), abs(lowlevel));
%         timestep  = 1/samplerate;
%         U1 = ones(size(rawdata));
%         for i = 1 : size(rawdata)
%            U1(i) = timestep*i;
%         end
%         U = [U1 rawdata];
%     end
% end


% U = Uquest; 
% 
% % Amplitude einstellen
% %U(:,2)=U(:,2)*amplitude/max(U(:,2));
% U(:,2)=U(:,2)*amplitude/(max(U(:,2))-min(U(:,2)));
%  
% % K = KL;
% 
% %Steigung in linearem Bereich bestimmen
% [N,i]=size(K);
% %5% der Kennlinie f�r Fit der Steigung
% l=0.2; % vorher 0.05
% %Runden
% n=round(N*l);
% 
% %Linearisierung um 0
% ind1=find(K(:,2)>=0,1);  %Index, an der Kennlinie durch 0 geht
% x=K(ind1:(ind1+n),1);   %n Punkte von da an f�r die Linearisierungsgerade verwenden
% y=K(ind1:(ind1+n),2);
% m=(sum(y.*x))/(sum(x.^2)); %Steigung
% 
% %-------> Falls U_steuer_max*m>U_Kmax: Fehler werfen oder Steigung
% %bestimmen zu U_Kmax/U_steuer(U_kmax) -> damit weiterrechnen -->
% %Vorverzerrung bei kleinen Amplituden = D�mpfung / Steuerspannung wird
% %soweit reduziert, bis maximale Ausgangsspannung mit gegebener Kennlinie
% %m�glich ist! -> Meldung ausgeben (Weiter verzerren / Abbrechen) und mit
% %modifiziertem m weiter rechnen
% if m*max(U(:,2))> max(K(:,2))      %Falls �ber die Kennlinie verzerrt w�rde: Linearisierungsgerade anpassen
%     m=max(K(:,2))/max(U(:,2));
% end
% if m*min(U(:,2))< min(K(:,2))       %auch im negativen Bereich
%     m=min(K(:,2))/min(U(:,2));
% end
% 
% %Puffer
% m=m*0.999;
% 
% %Kennlinie mit kubischen Splines fitten (Smoothing Parameter=1)
% U_Steuer=linspace(round(min(K(:,1))),round(max(K(:,1))),(round(max(K(:,1)))-round(min(K(:,1))))*1000+1); %paarweise U_Steuer-U_out in 0,001V Schritten
% %KL=csaps(K(:,1),K(:,2),1,U_Steuer);
% KL=spline(K(:,1),K(:,2),U_Steuer);
% Kennlinie=[U_Steuer', KL'];  
% U_vv=U;
% 
% %nichtlineare Vorverzerrung an der Kennlinie
% for ind=1:size(U(:,1))
%     U_a=m*U(ind,2);%gew�nschte Ausgangsspannung=Ui*m
%     l=find(Kennlinie(:,2)>=U_a,1);%in Kennlinie suchen -> Index l (Stelle, an der der Wert der Ausgangsspannung die gew�nschte Spannung �bersteigt)
%     U_vv(ind,2)=Kennlinie(l,1); %dem Zeitschritt die passende Steuerspannung zuordnen
% end
% 
% 
% %arb-Datei erzeugen
% data = U_vv(:,2);
% Uin = U_vv;
 

% 
% x=[-300  -299  -298  -297  -296];
% y=[ -433.2277 -432.2952 -431.3578 -430.4152 -429.4677];
% x=[1 5 0 32 8];
% y=[10 1 654 32 100];
% [~, index] = sort(x);
% Fq = griddedInterpolant(x(index), y(index));
% F =  griddedInterpolant(x(index), y(index));

Uin(:,1) = Uquest(:,1);

Uquest(:,2)=Uquest(:,2)*amplitude/(max(Uquest(:,2))-min(Uquest(:,2)));

[~, index] = sort(K(:,1));

%F = griddedInterpolant(K(index,2), K(index,1)); % original von Matlab
F = interp1(K(index,2), K(index,1));

Uin(:,2) = F(Uquest(:,2));





end

