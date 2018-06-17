function passed = test_compute_a_from_Uin_Uquest_300_jens()
  
    verbosity = 0;

    a_300_ideal = load('../../Python/nichtLinear/data/test_data/a_300_jens.csv');
    
    Uquest_300 = load('../../Python/nichtLinear/data/test_data/Uquest_300_jens.csv');        
    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    
    U_in(:,2) = setVpp_mV(U_in(:,2), 300);
    Uquest_300(:,2) = Uquest_300(:,2)*1000;
    
    a_300_computed = compute_a_from_Uin_Uquest( U_in(:,2), Uquest_300(:,2), 3, verbosity );
    
%     csvwrite('../../Python/nichtLinear/data/test_data/a_300_jens.csv',a_300_test);  
    
    err = norm(a_300_computed - a_300_ideal) / norm(a_300_ideal);
    
    passed = err<1e-2;

end