function [ a ] = compute_a_from_Uin_Uquest( Uin, Uout, N, verbosity )
%formely computeParams

l_in=length(Uin);
l_out=length(Uout);


[in] = overlay(Uin, Uout);

% l_in=length(Uin);
% l_out=length(Uout);
% %Signale übereinanderlegen --> Interpolation und Signale übereinander
% %legen: 
% %Interpolation
% x_in=linspace(1,l_out,l_in);
% x_out=linspace(1,l_out, l_out);
% Uin=interp1(x_in, Uin, x_out);
% %Signale übereinanderschieben -> über Kreuzkorrelation
% xc=xcorr(Uin, Uout);
% shift=find(xc==max(xc));
% 
% %if shift>=0
% %   in=u_in;
% %   out=in;
% %   out(1:l_out-shift)=u_out(shift+1:end);
% %   out(l_out-shift+1:end)=u_out(1:shift);
% %end
% 
% %if shift>=0
% %   out=u_out;
% %   in=out;
% %   in(1:l_out-shift)=u_in(shift+1:end);
% %   in(l_out-shift+1:end)=u_in(1:shift);
% %end
% 
% 
% if shift > length(Uout)
%     shift=length(Uout)-shift;
% end
% 
% if shift>=0
%    out=Uout;
%    in=out;
%    in(1:l_out-shift)=Uin(shift+1:end);
%    in(l_out-shift+1:end)=Uin(1:shift);
% end
% 
% if shift<0
%    out=Uout;
%    in=out;
%    in(l_out+shift+1:end)=Uin(1:-shift);
%    in(1:l_out+shift)=Uin(-shift+1:end);
% end


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
% Uout=1000*Uout;
% in=in_pp/(max(in)-min(in))*in;
 
 


%Spannungsmatrix erzeugen
U=zeros(l_out,N);
for ind=1:N
    U(:,ind)=in.^ind;
end

a=U\Uout;

if verbosity
    figure
    t=linspace(0,1/900000*1000000,length(in));
    plot(t,in,t,Uout)
    title('Spannungssignale')
    xlabel('t in us')
    ylabel('u in mV')
    legend('U_in', 'H^-1*U_out')
end

