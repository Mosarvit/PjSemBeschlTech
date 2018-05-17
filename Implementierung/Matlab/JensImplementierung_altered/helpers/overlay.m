function [in, out] = overlay (Uin, Uout)

l_in=length(Uin);
l_out=length(Uout);
%Signale übereinanderlegen --> Interpolation und Signale übereinander
%legen: 
%Interpolation
x_in=linspace(1,l_out,l_in);
x_out=linspace(1,l_out, l_out);
Uin=interp1(x_in, Uin, x_out);
%Signale übereinanderschieben -> über Kreuzkorrelation
xc=xcorr(Uin, Uout);
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


if shift > length(Uout)
    shift=length(Uout)-shift;
end

if shift>=0
   out=Uout;
   in=out;
   in(1:l_out-shift)=Uin(shift+1:end);
   in(l_out-shift+1:end)=Uin(1:shift);
end

if shift<0
   out=Uout;
   in=out;
   in(l_out+shift+1:end)=Uin(1:-shift);
   in(1:l_out+shift)=Uin(-shift+1:end);
end

end