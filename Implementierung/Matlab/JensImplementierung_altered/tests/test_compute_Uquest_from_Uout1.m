function passed = test_compute_Uquest_from_Uout()

    load('matlab_Workspace_nichtlin_VV_AR.mat');    
    load('u_quest_300.mat');

    u_quest_300_test=compute_Uquest_from_Uout(out_300, 900000, H); 
    
    err = norm(u_quest_300_test - u_quest_300) / norm(u_quest_300);
    passed = err<10e-3; 
end