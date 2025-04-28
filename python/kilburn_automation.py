import subprocess
import ADQL_queries

settings_file_name = '~/e-merlin/em_github/emerlin2caom/emerlin2caom2/settings_file.py'
data_sets = ['~/e-merlin/data/CY16204_C_001_20231117', '~/e-merlin/data/CY14205_C_001_20220901']
metadata_output = ['~/e-merlin/metadata/CY16204', '~/e-merlin/metadata/CY14205']
output_log_dir = '~/e-merlin/metadata/logs/'

### For when on the server and auto-generating places for the data
data_set_names = [x.split('/')[-1] for x in data_sets] # will break if there is a / at the end of the name
metadata_base = '~/e-merlin/metadata'
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
        f.write(new_settings_file.join('\n'))

for i, run in data_sets:
    alter_settings_file(settings_file_name, data_sets[i], metadata_output[i])
    with open(output_log_dir + data_set_names[i] + '_log.txt', 'w') as f:
        subprocess.call(['python', '-m', 'caom25', 'run_script.py'], stdout=f) # add step to delete after upload?
    timing, results = ADQL_queries.use_case_queries(url, use_case_nos)
    with open(output_log_dir + data_set_names[i] + '_timing.txt', w) as f:
        f.write('timing = {0}\nresults = {1}'.format(timing, results))









res, tim = ADQL_queries.use_case_queries(url, use_case_nos)

print(res)
print(tim)
