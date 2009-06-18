__author__ = "michal"
__date__ = "$2009-06-18 17:38:28$"

def _check_split(string, sep, parts):
    split = string.split(string, sep, parts - 1)
    if len(split) != parts:
        raise ValueError('string does not contains %d %r' % (parts - 1, sep))
    return split

def _fill_split(string, sep, parts, fill_with=''):
    ret = string.split(string, sep, parts - 1)
    mul = parts - len(ret)
    return ret + [fill_with] * mul

def split_proto(url):
    return _check_split(url, ':', 2)

def split_path(path):
    if path.startswith('//'):
        path = path[2:]
    return path.split('/')

def join_path(path):
    return '/' + '/'.join(path)

def _may_split_path(path):
    if isinstance(path, list):
        return False, path
    else:
        return True, split_path(path)

def _may_join_path(do, path):
    if do:
        return join_path(path)
    else:
        return path

def norm_path(path):
    stack = []
    splitten, path = _may_split_path(path)
    for item in path:
        if item == '' or item == '.':
            continue
        elif item == '..':
            if stack:
                stack.pop()
        else:
            stack.append(item)
    return _may_join_path(splitten, stack)

def split_host(rest):
    return _fill_split(rest, '/', 2)