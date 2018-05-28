function allTests()
    
    runAllTest();

    function runAllTest()        
        Folder = mfilename('fullpath');
        allFiles = dir('tests');    
        for i=1:numel(allFiles)
            filename = allFiles(i).name;
            lngth = size(filename,2);
            if lngth>3
              
                if is_octave ()
                  first4 = substr(filename,1,4);
                else
                  first4 = extractBetween(filename,1,4);
                end
                
                if strcmp(first4, 'test')                    
                    if is_octave ()                      
                      testFunName = char(substr(filename,1,lngth-2));
                    else                      
                      testFunName = char(extractBetween(filename,1,lngth-2));
                    end
                    executeTest(testFunName);
                end
            end
        end
    end  
end