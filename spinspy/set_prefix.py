from spinspy import local_data

def set_prefix(prefix):
    
    if prefix[-1] != '/':
        prefix += '/'

    local_data.prefix = prefix
