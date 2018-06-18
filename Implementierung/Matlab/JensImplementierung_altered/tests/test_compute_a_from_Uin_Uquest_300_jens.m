function passed = test_compute_a_from_Uin_Uquest_300_jens()
  
    verbosity = 0;

    a_300_ideal = load('../../Python/nichtLinear/data/test_data/a_param2_300.csv');
    
    Uquest_300_mV = load('../../Python/nichtLinear/data/test_data/Uquest_300_jens.csv');        
    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    
    Uin_mV = setVpp(U_in, 300);
    Uquest_300_mV(:,2) = Uquest_300_mV(:,2)*1000;
    
    a_300_computed = compute_a_from_Uin_Uquest( Uin_mV, Uquest_300_mV, 3, verbosity );
    
%     csvwrite('../../Python/nichtLinear/data/test_data/a_300_jens.csv',a_300_test);  
    
    err = norm(a_300_computed - a_300_ideal) / norm(a_300_ideal);
    
    passed = err<1e-2;

end