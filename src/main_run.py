from src import cleaning
from src import test_result_data_gen
from src import util

# ################################
# ################################
# ################################
# ################################
# CONFIGURATION

# configure the mongo_db server if you want
util.mongodb_server = "mongodb+srv://wmdb_temp:8EDM3sv5WiMBr26K@wmdb-01-7b21x.mongodb.net"
# util.mongodb_server = 'mongodb://localhost:27017'

# This sets the size of the training set
util.training_set_size = 86

# This defines how many entries are added to each file in the folder data/results when creating test results
number_of_test_result_data_entries = 10

# If you want to recreate the test result data set this to True
# Warning this may take VERY long if the number of entries is set to high
create_test_result_data = False

# If you want to run a duplicate detection set this to True
run_duplicate_detection = True

# ################################

# ################################
# ################################
# ################################






# ################################
# Code
if create_test_result_data:
    test_result_data_gen.create_test_result_data(number_of_test_result_data_entries)

if run_duplicate_detection:
    cleaning.run_duplicate_detection(verbose=True)
# ################################
