load('matlab_Workspace_nichtlin_VV_AR.mat');

[a, K] = Param_Signal2( U_in, 300, out_300, 3, H, 1);

err = norm(a - a_param2_300)