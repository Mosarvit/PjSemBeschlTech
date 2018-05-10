function printTestResult(passed, testName)
    if passed
       fprintf('PASSED : %s\n', testName);    
    else
       fprintf('FAILED : %s\n', testName);   
    end 
end

