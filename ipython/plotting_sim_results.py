import os

import matplotlib.pyplot as plt
import numpy as np

X = range(1,17)
requirements = ['DEC', 'PI', 'RA', 'UV', 'ancillary_target_name', 'ancillary_target_role', 'baseline', 'beam',
     'compute_available', 'correlator_setup', 'data_product_access', 'data_product_location', 'data_size',
     'dateTime', 'elevation', 'fov', 'frequency', 'input_parameters', 'memory_consumption', 'no_access',
     'no_backups', 'no_visits', 'observation_id', 'pipeline_name', 'pipeline_version', 'polarisation',
     'process_timing', 'project_code', 'quality', 'raw_data_access', 'raw_data_id', 'release_date',
     'resolution', 'runtime_environment', 'sensitivity', 'spectra', 'storage_available', 'target_name',
     'telescope', 'user_information', 'weather']

requirements.sort()

use_case_dict = {
    '1': ['target_name', 'RA', 'DEC', 'dateTime', 'frequency', 'spectra', 'baseline', 'resolution', 'beam', 'fov',
         'PI', 'telescope', 'no_visits', 'polarisation'],
    '2': ['quality', 'sensitivity', 'telescope', 'UV'],
    '3': ['pipeline_version', 'input_parameters', 'raw_data_id'],
    '4': ['project_code', 'PI', 'raw_data_id'],
    '5': ['RA', 'DEC', 'fov'],
    '6': ['ancillary_target_name', 'ancillary_target_role'],
    '7': ['pipeline_name', 'pipeline_version', 'raw_data_access', 'raw_data_id', 'data_product_access',
          'data_product_location', 'release_date', 'runtime_environment'],
    '8': ['compute_available', 'storage_available', 'memory_consumption', 'process_timing', 'data_size',
         'no_backups', 'no_access', 'raw_data_id'],
    '9': ['quality', 'input_parameters', 'process_timing', 'memory_consumption', 'raw_data_id'],
    '10': ['dateTime', 'RA', 'DEC', 'fov', 'polarisation', 'frequency', 'quality'],
    '11': ['release_date', 'raw_data_access', 'dateTime', 'PI', 'project_code', 'user_information'],
    '12': ['resolution', 'weather', 'dateTime', 'elevation', 'pipeline_name', 'pipeline_version', 'beam', 'UV',
          'baseline', 'sensitivity'],
    '13': ['raw_data_id', 'pipeline_name', 'pipeline_version', 'telescope', 'correlator_setup',
           'ancillary_target_role', 'ancillary_target_name', 'storage_available', 'compute_available',
          'PI', 'target_name'],
    '14': ['raw_data_id', 'pipeline_version', 'pipeline_name', 'quality', 'target_name', ],
    '15': ['release_date', 'observation_id', 'PI', 'data_product_access', 'raw_data_access'],
    '16': ['observation_id', 'process_timing', 'release_date']
}

# use_case_dict_actual = {
#     '1': ['telescope', 'baseline', 'RA', 'DEC', 'target_name', 'polarisation', 'dateTime', 'spectra', 'frequency',
#          'PI', 'resolution'], # not included - beam, fov, no_visits
#     '2': [], # no exisiting quality info so excluded
#     '3': ['pipeline_version', 'raw_data_id'], # input parameters not in CAOM
#     '4': ['project_code', 'PI', 'raw_data_id'], # PI returns nothing from emerlin
#     '5': ['RA', 'DEC'], # what is fov in radio?
#     '6': ['ancillary_target_name', 'ancillary_target_role'], # all inc
#     '7': ['pipeline_name', 'pipeline_version', 'raw_data_access', 'raw_data_id', 'data_product_access',
#          'data_product_location', 'release_date'], # no runtime_environment in caom
#     '8': ['process_timing', 'data_size', 'raw_data_id'], # no compute_available, storage_available, memory_consumption, no_access, no_backups
#     '9': ['process_timing', 'raw_data_id'], # no quality, input_parameters, memory_consumption
#     '10': ['dateTime', 'RA', 'DEC', 'polarisation', 'frequency'], # no fov, quality
#     '11': ['release_date', 'raw_data_access', 'dateTime', 'project_code', 'PI'], # PI iffy, no user_information
#     '12': ['dateTime', 'pipeline_name', 'pipeline_version', 'baseline'], # no resolution, weather, ?elevation?, beam, UV, sensitivity
#     '13': ['raw_data_id', 'pipeline_name', 'pipeline_version', 'raw_data_id'], # is a mess, come back to
#     '14': ['raw_data_id', 'pipeline_version', 'pipeline_name'], # no quality
#     '15': ['release_date', 'observation_id', 'PI', 'data_product_access', 'raw_data_access'], # complete
#     '16': ['observation_id', 'process_timing', 'release_date'] # complete
# }

use_case_dict_actual = {
    '1': ['telescope', 'baseline', 'RA', 'DEC', 'target_name', 'polarisation', 'dateTime', 'spectra', 'frequency',
         'PI', 'resolution', 'beam', 'fov', 'no_visits'], # not included - beam, fov, no_visits
    '2': ['sensitivity', 'telescope', 'UV'], # no exisiting quality info so excluded
    '3': ['pipeline_version', 'raw_data_id'], # input parameters not in CAOM
    '4': ['project_code', 'PI', 'raw_data_id'], # PI returns nothing from emerlin
    '5': ['RA', 'DEC', 'fov'], # what is fov in radio?
    '6': ['ancillary_target_name', 'ancillary_target_role'], # all inc
    '7': ['pipeline_name', 'pipeline_version', 'raw_data_access', 'raw_data_id', 'data_product_access',
         'data_product_location', 'release_date'], # no runtime_environment in caom
    '8': ['process_timing', 'data_size', 'raw_data_id'], # no compute_available, storage_available, memory_consumption, no_access, no_backups
    '9': ['process_timing', 'raw_data_id'], # no quality, input_parameters, memory_consumption
    '10': ['dateTime', 'RA', 'DEC', 'polarisation', 'frequency', 'fov'], # no fov, quality
    '11': ['release_date', 'raw_data_access', 'dateTime', 'project_code', 'PI'], # PI iffy, no user_information
    '12': ['resolution', 'dateTime', 'pipeline_name', 'pipeline_version', 'baseline', 'beam', 'UV', 'visibility', 'sensitivity', 'elevation'], # no resolution, weather, ?elevation?, beam, UV, sensitivity
    '13': ['raw_data_id', 'pipeline_name', 'pipeline_version', 'ancillary_target_role', 'ancillary_target_name', 'PI', 'target_name', 'telescope'], # is a mess, come back to
    '14': ['raw_data_id', 'pipeline_version', 'pipeline_name', 'target_name'], # no quality
    '15': ['release_date', 'observation_id', 'PI', 'data_product_access', 'raw_data_access'], # complete
    '16': ['observation_id', 'process_timing', 'release_date'] # complete
}

def create_uc_main(reqs, uc_dict):
    full_stack = []
    counter = 0
    sum_stack = []
    for uc in uc_dict.items():
        counter += 1
        full_stack.append([1 if x in uc[1] else 0 for x in reqs])
        mini_stack = [1 if x in uc[1] else 0 for x in reqs]
        mini_anno = ["{}_{}".format(x, y) for x, y in zip(mini_stack, reqs)]
        sum_stack.append(sum(mini_stack))
    full_array = np.array(full_stack)
    return full_array


def create_graph_results(results):
    Y = list(results.keys())
    X = list(results[Y[0]].keys())
    Z = []
    for x in Y:
        Z.extend(list(results[x].values()))

    x_ax, y_ax = np.meshgrid(X, Y)
    z_ar = np.asarray(Z)
    z_ax = z_ar.reshape(len(Y), len(X))

    plt.pcolormesh(X, Y, z_ax, vmax=1)
    plt.colorbar()
    plt.show()

def create_graph(X, Y, Z,vmax=None):
    plt.pcolormesh(X, Y, Z.T)
    plt.colorbar()
    plt.show()