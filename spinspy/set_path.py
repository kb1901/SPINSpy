from spinspy import local_data

def set_path(path):
    
    if path[-1] != '/':
        path += '/'

    local_data.path = path
