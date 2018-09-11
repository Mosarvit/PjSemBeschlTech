import nose

#  all_tezts runs all unit tests.
# It looks for all filex with the word "test" in it. Therefore the typo in its own name all_tezts is intentional to avoid recursion.

result = nose.run()