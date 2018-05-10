function passed = test_computeaK()

    load('matlab_Workspace_nichtlin_VV_AR.mat');
    load('u_quest_300.mat');

    [a, K] = computeaK( (U_in(:,2))', 300, u_quest_300, 3, 0);

    err = norm(a - a_param2_300) / norm(a_param2_300);
    
    passed = err<10e-3;

end