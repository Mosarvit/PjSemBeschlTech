function [ passed ] = test_compute_Uin_from_Uquest( )

    verbosity = 0;

    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    Uquest_300_ideal = load('../../Python/nichtLinear/data/testdata/Uquest_300.csv');
    
    Uin_300_computed=compute_Uin_from_Uquest(Uquest_300_ideal, K_param2_300, 300);   
    
%     in1 = Uin_300_computed(:,2)
    in1 = U_in(:,2);
    in2 = U_in(:,2);
    
    [Uin_300_computed] = overlay(in1, in2);
    
    Uin_300_computed = setVpp(Uin_300_computed, 1);
    U_300_ideal = setVpp( U_in(:,2), 1);
    
    if verbosity
        figure;
        plot(Uin_300_computed);       
        hold on;
        plot(U_300_ideal);
    end   
    
    err = norm(Uin_300_computed - U_300_ideal) / norm(U_300_ideal);
    passed = err<0.20; 

end
