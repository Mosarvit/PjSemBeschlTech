function [ U_Vpp ] = setVpp(Uin, Vpp) 

    U_Vpp = Uin;
    U_Vpp(:,2)=Uin(:,2)/(max(Uin(:,2))-min(Uin(:,2)))*Vpp;

end