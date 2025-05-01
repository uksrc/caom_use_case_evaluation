import subprocess
import ADQL_queries

settings_file_name = '/home/h14471mj/e-merlin/em_github/emerlin2caom/emerlin2caom2/settings_file.py'
data_set_file_base = '/home/h14471mj/e-merlin/data/'
metadata_base = '/home/h14471mj/e-merlin/metadata/'
data_set_names = ['CY16204_C_001_20231117', 'CY14205_C_001_20220901', 'CY10003_L_001_20210112',
             'CY10206_C_003_20200716_CASA5.8_tar4_OH', 'CY11218_K_005_20210430', 'CY14205_L_006_20230116',
             'CY9207_C_001_20190923', 'TS8004_C_001_20190801']
metadata_names = ['CY16204', 'CY14205', 'CY10003', 'CY10206_OH', 'CY11218', 'CY14205_L', 'CY9207', 'TS8004']
output_log_dir = '/home/h14471mj/e-merlin/metadata/logs/'

data_sets = [data_set_file_base + x for x in data_set_names]
metadata_output = [metadata_base + x for x in metadata_names]

### For when on the server and auto-generating places for the data
# metadata_output = [metadata_base + '/' + x for x in data_set_names]

# for x in metadata_output:
#   subprocess.call['mkdir', x]

url = "http://localhost:8080/tap"
use_case_nos = [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

def alter_settings_file(settings_file, data_loc, metadata_loc):
    with open(settings_file, 'r') as f:
        set_lines = f.readlines()
    new_settings_file = []
    for line in set_lines:
        if "storage_name = " in line:
            line = "storage_name = '{}'".format(data_loc)
        if "xmldir = " in line:
            line = "xmldir = '{}'".format(metadata_loc)
        new_settings_file.append(line)
    with open(settings_file, 'w') as f:
        f.write('\n'.join(new_settings_file))
        # f.write(new_settings_file.join('\n'))

for i, run in enumerate(data_sets):
    alter_settings_file(settings_file_name, data_sets[i], metadata_output[i])
    with open(output_log_dir + data_set_names[i] + '_log.txt', 'w') as f:
        subprocess.call(['run-emerlin'], stdout=f) # add step to delete after upload?
    timing, results = ADQL_queries.use_case_queries(url, use_case_nos)
    with open(output_log_dir + data_set_names[i] + '_timing.txt', 'w') as f:
        f.write('timing = {0}\nresults = {1}'.format(timing, results))

