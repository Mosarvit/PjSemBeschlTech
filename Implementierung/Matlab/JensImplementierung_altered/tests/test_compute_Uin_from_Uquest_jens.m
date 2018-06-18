function [ passed ] = test_compute_Uin_from_Uquest_jens( )

    verbosity = 0;

    Uin = load('../../Python/nichtLinear/data/test_data/Uin_jens.csv');
    Uin_300_ideal = setVpp( Uin, 300);
    
    K_300 = load('../../Python/nichtLinear/data/test_data/K_300_jens.csv');
    Uquest_300 = load('../../Python/nichtLinear/data/test_data/Uquest_300_jens.csv');
    Uquest_300_mV = Uquest_300;
    Uquest_300_mV(:,2) = Uquest_300(:,2)*1000;
    
    Uin_300_computed = compute_Uin_from_Uquest(Uquest_300_mV, K_300);  
    
%     if verbosity
%         figure;
%         plot(Uin_300_computed(:,2));
%         hold on;
%     end 
    
    [Uin_300_computed,~, Uin_300_ideal] = overlay(Uin_300_computed, Uin_300_ideal);
    
    if verbosity
        figure;
        plot(Uin_300_computed(:,2));       
        hold on; 
        plot(Uin_300_ideal(:,2));
    end   
    
    err = norm(Uin_300_computed(:,2) - Uin_300_ideal(:,2)) / norm(Uin_300_ideal(:,2));
    passed = err<0.20; 

end

