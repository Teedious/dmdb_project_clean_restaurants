from src import cleaning
from src import test_result_data_gen
from src import util

# ################################
# CONFIGURATION

util.training_set_size = 86
number_of_test_result_data_entries = 10

# If you want to recreate the test result data set this to True
# Warning this may take VERY long if the number of entries is set to high
create_test_result_data = False

# If you want to run a duplicate detection set this to True
run_duplicate_detection = True

# ################################


if create_test_result_data:
    test_result_data_gen.create_documentation_data(number_of_test_result_data_entries)

if run_duplicate_detection:
    cleaning.run_duplicate_detection(verbose=True)
