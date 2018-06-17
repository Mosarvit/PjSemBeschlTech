function passed = test_compute_K_from_a_300_our()

    verbosity = 0;

    K_300_ideal = load('../../Python/nichtLinear/data/test_data/K_300_our.csv');
    a_300 = load('../../Python/nichtLinear/data/test_data/a_300_our.csv');

    %
    
    K_300_test = compute_K_from_a( a_300, verbosity);
    
%     csvwrite('../../Python/nichtLinear/data/test_data/K_300_our.csv',K_300_test);  
    
    err = norm(K_300_test - K_300_ideal) / norm(K_300_ideal);     
    
    passed = err<10e-3;

end