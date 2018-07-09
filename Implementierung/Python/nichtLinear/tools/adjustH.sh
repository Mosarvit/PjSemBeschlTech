#!/bin/bash

dateiName='csvDateien_K/Uout_1.csv'
signal_output='Signal_output.csv'
fBB='5e6'
frev='9e5'
csv='1'

#Testing singlesine_Signal
python singlesine_Signal.py -i $dateiName -o $signal_output -frev $frev -fBB $fBB #--debug

#Testing singlesine_SineRef
sineref_output='SineRef_output.csv'
python singlesine_SineRef.py -i $signal_output -o $sineref_output -frev $frev -fBB $fBB -csv $csv #--debug

#Testing singlesine_Verzerrungszahlen
verzerrungszahlen_output='verzerrungszahlen_output.csv'
python singlesine_Verzerrungszahlen.py -i $dateiName -signal $signal_output -ref $sineref_output -o $verzerrungszahlen_output -frev $frev -fBB $fBB -csv $csv #--debug

# Testing singlesine_save_results
python singlesine_save_results.py -i $verzerrungszahlen_output -u '0' -o 'adjustH/results.csv'

#########################
#########################
dateiName='csvDateien_K/Uout_2.csv'
#Testing singlesine_Signal
python singlesine_Signal.py -i $dateiName -o $signal_output -frev $frev -fBB $fBB #--debug

#Testing singlesine_SineRef
sineref_output='SineRef_output.csv'
python singlesine_SineRef.py -i $signal_output -o $sineref_output -frev $frev -fBB $fBB -csv $csv #--debug

#Testing singlesine_Verzerrungszahlen
verzerrungszahlen_output='verzerrungszahlen_output.csv'
python singlesine_Verzerrungszahlen.py -i $dateiName -signal $signal_output -ref $sineref_output -o $verzerrungszahlen_output -frev $frev -fBB $fBB -csv $csv #--debug


# Testing singlesine_save_results
python singlesine_save_results.py -i $verzerrungszahlen_output -u '0' -o 'adjustH/results.csv'

#########################
#########################
dateiName='csvDateien_K/Uout_3.csv'
#Testing singlesine_Signal
python singlesine_Signal.py -i $dateiName -o $signal_output -frev $frev -fBB $fBB #--debug

#Testing singlesine_SineRef
sineref_output='SineRef_output.csv'
python singlesine_SineRef.py -i $signal_output -o $sineref_output -frev $frev -fBB $fBB -csv $csv #--debug

#Testing singlesine_Verzerrungszahlen
verzerrungszahlen_output='verzerrungszahlen_output.csv'
python singlesine_Verzerrungszahlen.py -i $dateiName -signal $signal_output -ref $sineref_output -o $verzerrungszahlen_output -frev $frev -fBB $fBB -csv $csv #--debug


# Testing singlesine_save_results
python singlesine_save_results.py -i $verzerrungszahlen_output -u '0' -o 'adjustH/results.csv'