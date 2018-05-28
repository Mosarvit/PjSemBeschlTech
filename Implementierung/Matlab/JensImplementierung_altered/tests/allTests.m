function allTests()
    
    runAllTest();

    function runAllTest()        
        Folder = mfilename('fullpath');
        allFiles = dir('tests');    
        for i=1:numel(allFiles)
            filename = allFiles(i).name;
            lngth = size(filename,2);
            if lngth>3
                first4 = substr(filename,1,4);
                if strcmp(first4, 'test')
                    testFunName = char(substr(filename,1,lngth-2));
                    executeTest(testFunName);
                end
            end
        end
    end
end