function passed = test_compute_Uquest_from_Uout_300_jens()

    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    Uquest_300 = load('../../Python/nichtLinear/data/test_data/Uquest_300_jens.csv');
  
    Hconv = H_a;
    Hconv(:,3) = H_p(:,2);
 
    Uquest_300_test=compute_Uquest_from_Uout(out_300, 900000, Hconv); 
    
%     csvwrite('../../Python/nichtLinear/data/test_data/Uquest_300_jens.csv',Uquest_300_test); 
    
    err = norm(Uquest_300_test - Uquest_300) / norm(Uquest_300);
    passed = err<1e-4; 
end