function passed = test_compute_Uquest_from_Uout_BBsignal_ideal()
 
    BBsignal_ideal = load('../../Python/nichtLinear/data/test_data/BBsignal_ideal.csv');
    Uquest_from_BBsignal_ideal = load('../../Python/nichtLinear/data/test_data/Uquest_from_BBsignal_our.csv');
    
    H_a = load('../../Python/nichtLinear/data/test_data/H_a_our.csv');
    H_p = load('../../Python/nichtLinear/data/test_data/H_p_our.csv');    
    Hconv = H_a;
    Hconv(:,3) = H_p(:,2);

    Uquest_from_BBsignal_computed=compute_Uquest_from_Uout(BBsignal_ideal, 900000, Hconv); 
    
%     csvwrite('../../Python/nichtLinear/data/test_data/Uquest_from_BBsignal_our.csv',Uquest_from_BBsignal_computed);  
    
    err = norm(Uquest_from_BBsignal_ideal - Uquest_from_BBsignal_computed) / norm(Uquest_from_BBsignal_ideal);
    passed = err<1e-4; 
end