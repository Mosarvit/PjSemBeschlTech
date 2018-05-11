function passed = test_compute_K_from_a()

    verbosity = 0;

    load('matlab_Workspace_nichtlin_VV_AR.mat');
    load('u_quest_300.mat');

    K = compute_K_from_a( a_param2_300, verbosity);
    
    err = norm(K - K_param2_300) / norm(K_param2_300);
    
    passed = err<10e-3;

end