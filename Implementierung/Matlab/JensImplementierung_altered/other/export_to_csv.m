load('matlab_Workspace_nichtlin_VV_AR.mat');

csvwrite('..\..\Python\nichtLinear\data\testdata\H_a.csv',H_a);
csvwrite('..\..\Python\nichtLinear\data\testdata\H_p.csv',H_p);
csvwrite('..\..\Python\nichtLinear\data\testdata\H.csv',H);
csvwrite('..\..\Python\nichtLinear\data\testdata\out_300.csv',out_300);
csvwrite('..\..\Python\nichtLinear\data\testdata\out_400.csv',out_400);

csvwrite('..\..\Python\nichtLinear\data\testdata\U_in.csv',U_in);

csvwrite('..\..\Python\nichtLinear\data\testdata\a_param2_300.csv',a_param2_300);
csvwrite('..\..\Python\nichtLinear\data\testdata\a_param2_400.csv',a_param2_400);

csvwrite('..\..\Python\nichtLinear\data\testdata\K_param2_300.csv',K_param2_300);
csvwrite('..\..\Python\nichtLinear\data\testdata\K_param2_400.csv',K_param2_400);