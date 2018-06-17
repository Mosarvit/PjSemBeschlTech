function passed = test_system_compute_K_from_Uin_Uout_300_jens()

    verbosity = 0;
    
    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    
    Uin_mV(:,2) = setVpp_mV(U_in(:,2), 300);
    Uout_300_mV = out_300*1000;
    
    H_a = load('../../Python/nichtLinear/data/test_data/H_a_jens.csv');
    H_p = load('../../Python/nichtLinear/data/test_data/H_p_jens.csv');    
    Hconv = H_a;
    Hconv(:,3) = H_p(:,2);
    
    K_300_ideal = K_param2_300;
    
    %
    
    Uquest_300_mV=compute_Uquest_from_Uout(Uout_300_mV, 900000, Hconv);
    a_300_test = compute_a_from_Uin_Uquest( Uin_mV(:,2), Uquest_300_mV(:,2), 3, verbosity );    
    K_300_test = compute_K_from_a( a_300_test, verbosity);
    
    err = norm(K_300_test - K_300_ideal) / norm(K_300_ideal);  
    
    passed = err<0.05;

end