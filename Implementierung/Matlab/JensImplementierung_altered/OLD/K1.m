function [ K ] = K1( b, du )
%Produziert eine Kennlinie aus den Eingabeparametern b (Vektor mit
%Koeffizienten) und dU ("Abtastung") im Intervall U_in=[-300mV;300mV]


M_=round(300/du);
M=M_*2+1;
K=zeros(M,2);
L=length(b);

for i=1:M
    K(i,1)=-M_+(i-1)*du;
    for ind=1:L
        K(i,2)=K(i,2)+b(ind)*K(i,1)^(ind);
    end
end

end

