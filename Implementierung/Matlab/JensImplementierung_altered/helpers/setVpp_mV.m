function [ Uvpp_mV ] = setVpp_mV(Uin, amplitude_mV) 

    Uvpp_mV=Uin/(max(Uin)-min(Uin))*amplitude_mV;

end