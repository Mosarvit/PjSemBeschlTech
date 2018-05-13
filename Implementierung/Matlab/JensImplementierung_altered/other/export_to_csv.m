load('matlab_Workspace_nichtlin_VV_AR.mat');

csvwrite('..\..\Python\nichtLinear\data\testdata\H_a.csv',H_a);
csvwrite('..\..\Python\nichtLinear\data\testdata\H_p.csv',H_p);
csvwrite('..\..\Python\nichtLinear\data\testdata\H.csv',H);
csvwrite('..\..\Python\nichtLinear\data\testdata\Uout_300.csv',out_300);
csvwrite('..\..\Python\nichtLinear\data\testdata\Uout_400.csv',out_400);

csvwrite('..\..\Python\nichtLinear\data\testdata\Uin.csv',U_in);

csvwrite('..\..\Python\nichtLinear\data\testdata\a_param2_300.csv',a_param2_300);
csvwrite('..\..\Python\nichtLinear\data\testdata\a_param2_400.csv',a_param2_400);

csvwrite('..\..\Python\nichtLinear\data\testdata\K_param2_300.csv',K_param2_300);
csvwrite('..\..\Python\nichtLinear\data\testdata\K_param2_400.csv',K_param2_400);

  
load('u_quest_400.mat');

u_quest_400_test=compute_Uquest_from_Uout(out_400, 900000, H); 

csvwrite('..\..\Python\nichtLinear\data\testdata\Uquest_400.csv',u_quest_400_test);

load('u_quest_300.mat');

u_quest_300_test=compute_Uquest_from_Uout(out_300, 900000, H); 

csvwrite('..\..\Python\nichtLinear\data\testdata\Uquest_300.csv',u_quest_300_test);