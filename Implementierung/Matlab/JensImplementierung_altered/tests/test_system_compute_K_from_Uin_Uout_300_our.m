function passed = test_system_compute_K_from_Uin_Uout_300_our()

    verbosity = 0;
    
    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    
    K_300_ideal = load('../../Python/nichtLinear/data/test_data/K_300_our.csv');
    
    Uin = load('../../Python/nichtLinear/data/test_data/Uin_our.csv');
    Uin_mV(:,2) = setVpp_mV(Uin(:,2), 300);
    
    Uout_300 = load('../../Python/nichtLinear/data/test_data/Uout_300_our.csv');
    Uout_300_mV =  Uout_300*1000;
    
    H_a = load('../../Python/nichtLinear/data/test_data/H_a_our.csv');
    H_p = load('../../Python/nichtLinear/data/test_data/H_p_our.csv');    
    Hconv = H_a;
    Hconv(:,3) = H_p(:,2);
    
    %
    
    Uquest_300_mV=compute_Uquest_from_Uout(Uout_300_mV, 900000, Hconv);
    a_300_test = compute_a_from_Uin_Uquest( Uin_mV(:,2), Uquest_300_mV(:,2), 3, verbosity ); 
    K_300_test = compute_K_from_a( a_300_test, verbosity);
    
    err = norm(K_300_test - K_300_ideal) / norm(K_300_ideal);  
    
    passed = err<1e-4;

end