close all
clear 
%% Parameter
f_rep=900e3;
f_bb=5e6;
f_g=80e6;
Samplingrate=1e9;
wrev=2*pi*f_rep;
wbb=2*pi*f_bb;
x=wbb/wrev;
w=linspace(f_rep, floor(f_g/f_rep)*f_rep, floor(f_g/f_rep));
dt=1/Samplingrate;
t=linspace(0,1/f_rep, round(1/f_rep/dt));
%% Einlesen
%Referenzeingangssignal einlesen
[t_in1, u_in1]=readarb('Uefkt_EXP106_900kHz_5MHz.arb');
%Übertragungsfunktion Referenz einlesen
Href = csvread('Uefkt_EXP106.csv');
%andere Referenz?
H_ = csvread('Uefkt_exp155b.csv');
[t_in2, u_in2]=readarb('Uefkt_exp155b_110kHz_1.5MHz.arb');
%% Plot Phase
w1=Href(:,1);
a1=Href(:,2);
p1=Href(:,3);
w2=H_(:,1);
a2=H_(:,2);
p2=H_(:,3);
figure
plot(w2,p2)
%% bereinigen
p3=p2;
for ind=1:length(p2)-1
    if p2(ind)*p2(ind+1)<0
        if p2(ind)>pi/2 && p2(ind+1)<-pi/2
            p3(ind+1:end)=p3(ind+1:end)+2*pi;
        elseif p2(ind)<-pi/2 && p2(ind+1)>pi/2
            p3(ind+1:end)=p3(ind+1:end)-2*pi;
        end
    end
end
figure
plot(w2,p3)
%% interpolieren und plotten
H=interp1(w2, a2, w, 'linear');
arg=interp1(w2, p3, w, 'linear');
figure
plot(w,arg)
%% vorverzerren
u_in=zeros(1, length(t));
U=u_in;
for ind=1:length(w)
   b=-f_rep/f_bb*(sinc((ind*2*f_rep-2*f_bb)/f_bb/2)-sinc((ind*2*f_rep+2*f_bb)/f_bb/2));
   u_in=u_in+b/H(ind)*sin(ind*2*pi*f_rep*t-ones(1,length(t))*arg(ind));
   U=U+b*sin(ind*2*pi*f_rep*t);
end
figure
plot(t,u_in)
figure
plot(t,U)
figure
plot(t_in2,u_in2)