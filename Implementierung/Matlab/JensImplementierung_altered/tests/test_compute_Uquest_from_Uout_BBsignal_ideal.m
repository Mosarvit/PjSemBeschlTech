function passed = test_compute_Uquest_from_Uout_BBsignal_ideal()

    load('data/matlab_Workspace_nichtlin_VV_AR.mat');
    BBsignal_ideal = load('../../Python/nichtLinear/data/test_data/BBsignal_ideal.csv');
    Uquest_from_BBsignal_ideal = load('../../Python/nichtLinear/data/test_data/Uquest_from_BBsignal_ideal.csv');

    Uquest_from_BBsignal_computed=compute_Uquest_from_Uout(BBsignal_ideal, 900000, H); 
    
    err = norm(Uquest_from_BBsignal_ideal - Uquest_from_BBsignal_computed) / norm(Uquest_from_BBsignal_ideal);
    passed = err<1e-4; 
end