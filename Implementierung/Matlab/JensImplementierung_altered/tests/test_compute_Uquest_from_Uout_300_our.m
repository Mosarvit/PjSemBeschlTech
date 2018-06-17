function passed = test_compute_Uquest_from_Uout_300_our()
 
    Uout_300 = load('../../Python/nichtLinear/data/test_data/Uout_300_our.csv');
    Uquest_300_ideal = load('../../Python/nichtLinear/data/test_data/Uquest_300_our.csv');
    
    H_a = load('../../Python/nichtLinear/data/test_data/H_a_our.csv');
    H_p = load('../../Python/nichtLinear/data/test_data/H_p_our.csv');    
    Hconv = H_a;
    Hconv(:,3) = H_p(:,2);
    
    Uquest_300_test=compute_Uquest_from_Uout(Uout_300, 900000, Hconv); 
    
%     csvwrite('../../Python/nichtLinear/data/test_data/Uquest_300_our.csv',Uquest_300_test);  
    
    err = norm(Uquest_300_test - Uquest_300_ideal) / norm(Uquest_300_ideal);
    passed = err<10e-3; 
end