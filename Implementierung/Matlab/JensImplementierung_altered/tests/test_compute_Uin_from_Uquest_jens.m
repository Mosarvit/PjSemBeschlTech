function [ passed ] = test_compute_Uin_from_Uquest_jens( )

    verbosity = 0;

    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    Uquest_300_ideal = load('../../Python/nichtLinear/data/test_data/Uquest_300_jens.csv');
    
    Uin_300_computed=compute_Uin_from_Uquest(Uquest_300_ideal, K_param2_300);   
   
    [Uin_300_computed] = overlay(Uin_300_computed(:,2), U_in(:,2));
    
    Uin_300_computed = setVpp_mV(Uin_300_computed, 1);
    U_300_ideal = setVpp_mV( U_in(:,2), 1);
    
    if verbosity
        figure;
        plot(Uin_300_computed);       
        hold on;
        plot(U_300_ideal);
    end   
    
    err = norm(Uin_300_computed - U_300_ideal) / norm(U_300_ideal);
    passed = err<0.20; 

end

