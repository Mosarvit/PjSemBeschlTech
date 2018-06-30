#!/bin/bash
dateiName='C1--Trace--00000.trc'
bcfName='C1--Trace--00000.bcf'
python rfconvert_trc2bcf.py -i $dateiName -o $bcfName

csvName='C1--Trace--00000.csv'
python rfconvert_bcf2csv.py -i $bcfName -o $csvName

signal_output='Signal_output.bcf'
fBB='5e6'
frev='9e5'
csv='1'

#Testing singlesine_Signal with the csv file
python singlesine_Signal.py -i $csvName -o $signal_output -frev $frev -fBB $fBB -csv $csv --debug

#Testing singlesine_Signal with the bcf file
python singlesine_Signal.py -i $bcfName -o $signal_output -frev $frev -fBB $fBB -csv $csv --debug

#Testing singlesine_SineRef
#sineref_output='SineRef_output.bcf'
#python singlesine_SineRef.py -i $signal_output -o $sineref_output -frev $frev -fBB $fBB -csv $csv --debug

#Testing singlesine_Verzerrungszahlen
#verzerrungszahlen_output='verzerrungszahlen_output.bcf'
#python singlesine_Verzerrungszahlen.py -i $dateiName -signal $signal_output -ref $sineref_output -o $verzerrungszahlen_output -frev $frev -fBB $fBB -csv $csv --debug
