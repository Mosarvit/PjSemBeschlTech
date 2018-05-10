function passed = test_computeU_quest()

    load('matlab_Workspace_nichtlin_VV_AR.mat');    
    load('u_quest_300.mat');

    u_quest_300_test=computeU_quest(out_300, 900000, H);  
    
    err = norm(u_quest_300_test - u_quest_300) / norm(u_quest_300);
    passed = err<10e-3; 
end