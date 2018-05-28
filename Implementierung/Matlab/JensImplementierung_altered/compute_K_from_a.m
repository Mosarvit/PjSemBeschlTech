function [ K ] = compute_K_from_a( a, verbosity )

    b=a;
    du=1;
    
    M_=round(300/du);
    M=M_*2+1;
    K=zeros(M,2);
    L=length(b);

    for i=1:M
        K(i,1)=-M_+(i-1)*du;
        for ind=1:L
            K(i,2)=K(i,2)+b(ind)*K(i,1)^(ind);
        end
    end
    
    if verbosity
        figure;
        plot(K(:,1),K(:,2));
        title('Kennlinie')
        xlabel('U_in in mV')
        ylabel('U_out in mV')
    end

end

