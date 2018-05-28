function [ passed ] = test_compute_Uin_from_Uquest( )

    verbosity = 0;

    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    Uquest_300 = load('../../Python/nichtLinear/data/testdata/Uquest_300.csv');
    
    Uin_300_computed=compute_Uin_from_Uquest(Uquest_300, K_param2_300, 300);   
    
    [U_computed, U_ideal] = overlay(Uin_300_computed(:,2), U_in(:,2));
    
    U_computed = setVpp(U_computed, 1);
    U_ideal = setVpp(U_ideal, 1);
    
    if verbosity
        figure;
        plot(U_computed);       
        hold on;
        plot(U_ideal);
    end   
    
    err = norm(U_computed - U_ideal) / norm(U_ideal);
    passed = err<0.20; 

end

