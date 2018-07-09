#!/bin/bash

#dateiName='singleSineTest_mod.csv'
#dateiName='singleSineTest_Orginal.csv'
dateiName='csvDateien_K/Messung_060_TD_y_1.csv'
#dateiName='csvDateien_J3dB/rs_u_out_020mvpp_3dB.csv'
#dateiName='csvDateien_M/Uefkt_Exp120_4000kHz_5Mhz_mth1.csv'
#dateiName='output_test.csv'
signal_output='Signal_output.csv'
fBB='5e6'
frev='9e5'
csv='1'
#Testing singlesine_Signal
python singlesine_Signal.py -i $dateiName -o $signal_output -frev $frev -fBB $fBB --debug

#Testing singlesine_SineRef
sineref_output='SineRef_output.csv'
python singlesine_SineRef.py -i $signal_output -o $sineref_output -frev $frev -fBB $fBB -csv $csv --debug

#Testing singlesine_Verzerrungszahlen
verzerrungszahlen_output='verzerrungszahlen_output.csv'
python singlesine_Verzerrungszahlen.py -i $dateiName -signal $signal_output -ref $sineref_output -o $verzerrungszahlen_output -frev $frev -fBB $fBB -csv $csv --debug


# Testing singlesine_save_results
python singlesine_save_results.py -i $verzerrungszahlen_output -u '0' -o 'results.csv'



#Testing singlesine_Bewertung
#flag='csvDateien_K/Messung_060_TD_y_1.csv'
#flag='singleSineTest_Orginal.csv'
#bewertung_output='Bewertung_output.csv'
#python singlesine_Bewertung.py -f $flag -o $bewertung_output -frev $frev -fBB $fBB -csv $csv --debug

#Testing singlesine_EingabeDatei
#Kerstin
#input_file='Eingabe_K.txt'
#folder_name='csvDateien_K'
#python singlesine_EingabeDatei.py -i $input_file -f $folder_name -u 1

#M
#input_file='Eingabe_M.txt'
#folder_name='csvDateien_M'
#python singlesine_EingabeDatei.py -i $input_file -f $folder_name -u 1

#J3dB
#input_file='Eingabe_J3dB.txt'
#folder_name='csvDateien_J3dB'
#python singlesine_EingabeDatei.py -i $input_file -f $folder_name -u 1
