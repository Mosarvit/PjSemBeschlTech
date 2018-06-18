function passed = test_compute_a_from_Uin_Uquest_300_our()
     
    verbosity = 0;
 
    Uin_our = load('../../Python/nichtLinear/data/test_data/Uin_our.csv');
    Uin_our = setVpp(Uin_our, 300);
    
    Uquest_300 = load('../../Python/nichtLinear/data/test_data/Uquest_300_our.csv');
    Uquest_300_mV = Uquest_300*1000;
    
    a_300_ideal = load('../../Python/nichtLinear/data/test_data/a_300_our.csv');
    
    %
    
    a_300_test = compute_a_from_Uin_Uquest( Uin_our, Uquest_300_mV, 3, verbosity );    
    
%     csvwrite('../../Python/nichtLinear/data/test_data/a_300_our.csv',a_300_test);  
    
    err = norm(a_300_ideal - a_300_test) / norm(a_300_test);    
    passed = err<10e-3;

end