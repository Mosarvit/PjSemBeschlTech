function [ u_in ] = U_inp3( U_out, f_rep, H_ )
%Berechnet das Eingangssignal eines Spannugnssignals U_out (eine
%Periodenlänge der Periodendauer 1/f_rep) basierend auf der
%Übertragungsfunktion, die im Quelltect dieser Funktion angegeben ist.
%Unterschied Vers 1: ÜF variable (Pfad)
%Unterschied Vers 2: ÜF wird direkt übergeben. Format: [f, H(komplex)]

%Übertragungsfkt:
%H_=csvread(Pfad);

f_max=floor(max(H_(:,1))/f_rep)*f_rep;

 %u_in,f_rep, f_grenz, Samplingrate)
%Änderung zu U_out: Grenzfrequenz f_grenz variabel, nicht mehr fest bei 80
%MHz
%   Detailed explanation goes here
%Berechnete das Ausgangssignal zu einem Eingagnssignal u_in (2
%Periodenlängen 1/f_rep)

w=linspace(f_rep, f_max, f_max/f_rep);
dt=1/f_rep/length(U_out);
t=linspace(0,1/f_rep, round(1/f_rep/dt));

%H=spline(H_(:,1), H_(:,2), w);
%arg=interp1(H_(:,1), H_(:,3), w, 'linear')/180*pi;
H_neu=interp1(H_(:,1), H_(:,2), w);
H=abs(H_neu);
arg=angle(H_neu);%/180*pi;

%Fehler, falls über die Grenze hinaus interpoliert werden soll -> Manuell
%korrigieren
%for ind1=1:length(w)
%    if w(ind1)>H_(length(H_),1)
%        arg(ind1)=H_(length(H_),3)/180*pi;
%    end
%end

%u=u_in(1:length(u_in)/2);
u=U_out;

L=length(u);
NFFT=L;
ufft=fft(u,NFFT);
Y=2*ufft/L;
%fr=f_sample/2*linspace(0,1,round(NFFT/2)+1);

%Gleichanteil des Signals --> weg - u_out=zeros(1, length(t));
%u_out=ones(1, length(t))*Y(1);
u_in=zeros(1, length(t));

if size(Y,1)==1
    Y = Y';
else
    
u_dim2 = size(Y,2);
 

figure
for ind=1:f_max/f_rep
    %Achtung: U_out NX2 Matrix (Zeit und Spannung): Dieser Block
    a_n=Y(ind+1,u_dim2)+Y(end+1-ind,u_dim2);
    b_n=1i*(Y(ind+1,u_dim2)-Y(end+1-ind,u_dim2));
    
    omegat = 2*pi*ind*f_rep*t;
    gamma = ones(1,length(t))*(arg(ind));
    phi = omegat - gamma;
    
    c = 1/abs(H(ind))*( a_n*cos(phi) + b_n*sin(phi) ); 
    
    u_in = u_in + c;
    
%     a_n=Y(ind+1)+Y(end+1-ind);    
%     b_n=1i*(Y(ind+1)-Y(end+1-ind));    
%     u_in=u_in+1/abs(H(ind))*(a_n*cos(2*pi*ind*f_rep*t-ones(1,length(t))*(arg(ind)))+b_n*sin(2*pi*ind*f_rep*t-ones(1,length(t))*(arg(ind))));
    
    %u_in=u_in+abs(Y(ind+1))/H(ind)*sin(2*pi*ind*f_rep*t+ones(1,length(t))*(-arg(ind)+angle(Y(ind+1))));
    %%%%COMPLEX%%%%%
    %c_n=Y(ind+1,2);
    %c_minus_n=Y(end+1-ind,2);
    %u_n=(c_n+c_minus_n)./H_neu;
    %u_in=u_in+u_n;
    
    a = 1;    
end
b = u_in(end) ;
plot(u_in)

end

