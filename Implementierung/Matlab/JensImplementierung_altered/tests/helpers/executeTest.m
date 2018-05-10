function executeTest(testName)
    [passed] = feval(testName);
    printTestResults(passed, testName);
    clear all;
end
