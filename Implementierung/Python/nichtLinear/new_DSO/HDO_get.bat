python dso_get.py -r USB0::0x05FF::0x1023::3808N60406::INSTR -t 2 -o test.bcf -d 1 -c 1
python plot.py -i test.bcf
pause