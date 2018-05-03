load('matlab_Workspace_nichtlin_VV_AR.mat');
load('u_quest_300.mat');

[a, K] = computeParams( (U_in(:,2))', 300, u_quest_300, 3, 0);

err = norm(a - a_param2_300)