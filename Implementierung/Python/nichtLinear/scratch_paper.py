from adts import transfer_function
from helpers.csvHelper import read_in_transfer_function, save_transfer_function, read_in_transfer_function_old

H = read_in_transfer_function_old('data/test_data/H_a_our.csv', 'data/test_data/H_p_our.csv' )
save_transfer_function(H, 'data/test_data/H_our.csv')
