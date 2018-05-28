function passed = test_compute_a_from_Uin_Uquest()
     
    verbosity = 0;

    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    Uquest_300 = load('../../Python/nichtLinear/data/testdata/Uquest_300.csv');

%    keyboard;
    
    a = compute_a_from_Uin_Uquest( U_in(:,2)', 300, Uquest_300(:,2), 3, verbosity );
    
    err = norm(a - a_param2_300) / norm(a_param2_300);
    
    passed = err<10e-3;

end