function passed = test_compute_a_from_Uin_Uquest()

    verbosity = 0;

    load('matlab_Workspace_nichtlin_VV_AR.mat');
    load('u_quest_300.mat');

    a = compute_a_from_Uin_Uquest( (U_in(:,2))', 300, u_quest_300, 3, verbosity );
    
    err = norm(a - a_param2_300) / norm(a_param2_300);
    
    passed = err<10e-3;

end