load('matlab_Workspace_nichtlin_VV_AR.mat');

u_quest_300=U_inp3(out_300, 900000, H);
csvwrite('..\..\Python\nichtLinear\testdata\u_quest_300.csv',u_quest_300);
save('u_quest_300');

u_quest_400=U_inp3(out_400, 900000, H);
csvwrite('..\..\Python\nichtLinear\testdata\u_quest_400.csv',u_quest_400);
save('u_quest_400');