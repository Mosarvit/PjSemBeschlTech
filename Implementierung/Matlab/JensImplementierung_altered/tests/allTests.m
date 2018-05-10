function allTests()
    
    runAllTest();

    function runAllTest()        
        Folder = mfilename('fullpath');
        Folder = fullfile(Folder, '..');
        allFiles = dir(Folder);        
        for i=1:numel(allFiles)
            filename = allFiles(i).name;
            lngth = size(filename,2);
            if lngth>3
                first4 = extractBetween(filename,1,4);
                if strcmp(first4, 'test')
                    testFunName = char(extractBetween(filename,1,lngth-2));
                    executeTest(testFunName);
                end
            end
        end
    end
end