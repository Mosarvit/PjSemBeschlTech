function passed = test_compute_Uquest_from_Uout()

    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    Uquest_300 = load('../../Python/nichtLinear/data/testdata/Uquest_300.csv');

    Uquest_300_test=compute_Uquest_from_Uout(out_300, 900000, H); 
    
    err = norm(Uquest_300_test - Uquest_300) / norm(Uquest_300);
    passed = err<10e-3; 
end