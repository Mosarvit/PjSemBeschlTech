function [ Uquest ] = compute_Uquest_from_Uout( Uout, f_rep, H )


%Berechnet das Eingangssignal eines Spannugnssignals U_out (eine
%Periodenl�nge der Periodendauer 1/f_rep) basierend auf der
%�bertragungsfunktion, die im Quelltect dieser Funktion angegeben ist.
%Unterschied Vers 1: �F variable (Pfad)
%Unterschied Vers 2: �F wird direkt �bergeben. Format: [f, H(komplex)]

%�bertragungsfkt:
%H_=csvread(Pfad);

f_max=floor(max(H(:,1))/f_rep)*f_rep;

 %u_in,f_rep, f_grenz, Samplingrate)
%�nderung zu U_out: Grenzfrequenz f_grenz variabel, nicht mehr fest bei 80
%MHz
%   Detailed explanation goes here
%Berechnete das Ausgangssignal zu einem Eingagnssignal u_in (2
%Periodenl�ngen 1/f_rep)

w=linspace(f_rep, f_max, f_max/f_rep);
dt=1/f_rep/length(Uout);
t=round(linspace(0,1/f_rep,1/f_rep/dt).* 10e18) ./ 10e18;

% Uquest(:,1)=t;
% 
% %H=spline(H_(:,1), H_(:,2), w);
% %arg=interp1(H_(:,1), H_(:,3), w, 'linear')/180*pi;
% 
% %     Hconv(:,2) = abs(H(:,2));
% %     Hconv(:,3) = angle(H(:,2))/180*pi;
% 
% % Hamp=abs(H_neu);
% 
% % Hamp2=abs(H(:,2));
% Hph=angle(H(:,2));
% 
% % Hamp2=interp1(H(:,1), Hamp2, w);
% Hph=interp1(H(:,1), Hph, w);
% 
% hold on;
% plot(Hph)
% % plot(H_p)
% plot(H_p(:,2))
% 
% 
% 
% 
% H_neu=interp1(H(:,1), H(:,2), w);
% Hamp=abs(H_neu);
% Hph=angle(H_neu);%/180*pi;
% 
% % plot(Hph)
% % plot(Hamp)
% hold off;




H_neu=interp1(H(:,1), H(:,2:3), w);
Hamp=H_neu(:,1);
Hph=H_neu(:,2);



%Fehler, falls �ber die Grenze hinaus interpoliert werden soll -> Manuell
%korrigieren
%for ind1=1:length(w)
%    if w(ind1)>H_(length(H_),1)
%        arg(ind1)=H_(length(H_),3)/180*pi;
%    end
%end

%u=u_in(1:length(u_in)/2);
u=Uout;
Uquest = Uout;

L=length(u);
NFFT=L;
ufft=fft(u,NFFT);
Y=2*ufft/L;
%fr=f_sample/2*linspace(0,1,round(NFFT/2)+1);

%Gleichanteil des Signals --> weg - u_out=zeros(1, length(t));
%u_out=ones(1, length(t))*Y(1);
Uquest(:,2)=zeros(1, length(t));

if size(Y,1)==1
    Y = Y';
end
    
u_dim2 = size(Y,2);
 
 
for ind=1:f_max/f_rep
    %Achtung: U_out NX2 Matrix (Zeit und Spannung): Dieser Block
    a1 = Y(ind+1,u_dim2);
    a2 = Y(end+1-ind,u_dim2);
    
    b1 = Y(ind+1,u_dim2);
    b2 = Y(end+1-ind,u_dim2);
    
    a_n=Y(ind+1,u_dim2)+Y(end+1-ind,u_dim2);
    b_n=1i*(Y(ind+1,u_dim2)-Y(end+1-ind,u_dim2));
    
    omegat = 2*pi*ind*f_rep*t;
    gamma = ones(1,length(t))*(Hph(ind));
    phi = omegat - gamma;
    
    c = 1/abs(Hamp(ind))*( a_n*cos(phi) + b_n*sin(phi) ); 
    
    Uquest(:,2) = Uquest(:,2) + c';
    
%     a_n=Y(ind+1)+Y(end+1-ind);    
%     b_n=1i*(Y(ind+1)-Y(end+1-ind));    
%     u_in=u_in+1/abs(H(ind))*(a_n*cos(2*pi*ind*f_rep*t-ones(1,length(t))*(arg(ind)))+b_n*sin(2*pi*ind*f_rep*t-ones(1,length(t))*(arg(ind))));
    
    %u_in=u_in+abs(Y(ind+1))/H(ind)*sin(2*pi*ind*f_rep*t+ones(1,length(t))*(-arg(ind)+angle(Y(ind+1))));
    %%%%COMPLEX%%%%%
    %c_n=Y(ind+1,2);
    %c_minus_n=Y(end+1-ind,2);
    %u_n=(c_n+c_minus_n)./H_neu;
    %u_in=u_in+u_n;
    
end

end

