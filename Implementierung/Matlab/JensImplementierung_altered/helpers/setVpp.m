function [ Uvpp ] = setVpp(Uin, amplitude) 

    Uvpp=Uin/(max(Uin)-min(Uin))/1000*amplitude;

end