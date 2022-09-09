# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

def add_query_params(url, params):
    # params is a list of dictionaries where each dictionary contains the param 'name' and 'value'
    valid_param_found = False
    for param in params:
        param_name = param['name']
        param_value = param['value']
        if param_name is not None and param_value is not None:
            if valid_param_found:
                url = url + "&" + param_name + "=" + param_value
            else:
                url = url + "?" + param_name + "=" + param_value
            valid_param_found = True

    return url