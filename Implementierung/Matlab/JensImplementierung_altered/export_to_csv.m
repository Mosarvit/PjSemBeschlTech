load('matlab_Workspace_nichtlin_VV_AR.mat');

csvwrite('..\..\Python\nichtLinear\testdata\H_a.csv',H_a);
csvwrite('..\..\Python\nichtLinear\testdata\H_p.csv',H_p);
csvwrite('..\..\Python\nichtLinear\testdata\H.csv',H);
csvwrite('..\..\Python\nichtLinear\testdata\out_300.csv',out_300);
csvwrite('..\..\Python\nichtLinear\testdata\out_400.csv',out_400);

csvwrite('..\..\Python\nichtLinear\testdata\U_in.csv',U_in);

csvwrite('..\..\Python\nichtLinear\testdata\a_param2_300.csv',a_param2_300);
csvwrite('..\..\Python\nichtLinear\testdata\a_param2_400.csv',a_param2_400);

csvwrite('..\..\Python\nichtLinear\testdata\K_param2_300.csv',K_param2_300);
csvwrite('..\..\Python\nichtLinear\testdata\K_param2_400.csv',K_param2_400);