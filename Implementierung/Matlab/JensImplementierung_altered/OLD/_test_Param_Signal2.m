function passed = test_Param_Signal2()

    load('matlab_Workspace_nichtlin_VV_AR.mat');

    [a, K] = Param_Signal2( U_in, 300, out_300, 3, H, 0);

    err = norm(a - a_param2_300) / norm(a_param2_300);    
    passed = err<10e-3; 
end