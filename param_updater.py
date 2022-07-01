"""
to call: python3 param_updater.py <project_folder_name> <start_date in iso format> <end_date in iso format> <start_cash in integer format> <param_to_optimize 1 name> <param_to_optimize 1 value> ...
"""
import json
import sys
import os

# make sure we have the right amount of arguments
assert(len(sys.argv) % 2 == 1)

proj_name = sys.argv[1]
start_date_str_iso = sys.argv[2]
end_date_str_iso = sys.argv[3]
start_cash_str = sys.argv[4]

path_to_config_file = os.path.join(f'{proj_name}', 'config.json')
with open(path_to_config_file) as config_file:
    config_dict = json.load(config_file)

# get init params into param_dict
param_dict = config_dict['parameters']
param_dict['start_date'] = start_date_str_iso
param_dict['end_date'] = end_date_str_iso
param_dict['start_cash'] = start_cash_str

# get params to optimize and add to param_dict
opt_names = list()
opt_vals = list()
for i in range(5, len(sys.argv)):
    if i % 2 == 1:
        # we have a param name
        opt_names.append(sys.argv[i])
    else:
        # we have a value
        opt_vals.append(sys.argv[i])
opt_tups = zip(opt_names, opt_vals)

for key, val in opt_tups:
    param_dict[key] = val

with open(path_to_config_file, 'w') as config_file:
    json.dump(config_dict, config_file)

