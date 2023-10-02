import re
import keyword

def is_xid_start(s: str) -> bool:
    return s.isidentifier()

def is_xid_continue(s: str) -> bool:
    return f'_{s}'.isidentifier()

def str_to_raw_id(s: str) -> str:
    s = s.lstrip()
    assert s != ''

    if s.isascii():
        s = re.sub(r'[^A-Za-z_0-9]', '_', s)
        s = re.sub(r'^[0-9]', r'_\0', s, count=1)
    else:
        s = re.sub(r'[\S\s]', lambda m: m.group(0) if is_xid_continue(m.group(0)) else '_', s)
        if not is_xid_start(s[0]):
            s = f'_{s}'
    s = re.sub(r'__+', '_', s)
    s = s.rstrip('_')
    
    if keyword.iskeyword(s):
        s += '_'
    
    return s

def id_to_lower(id: str) -> str:
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', id).lower()

def id_to_camel(id: str) -> str:
    return re.sub(r'_([a-zA-Z])', lambda m: m.group(1).upper(), id)

def id_to_upper(id: str) -> str:
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', id).upper()

def str_to_mod_id(s: str) -> str:
    return id_to_lower(str_to_raw_id(s))

def str_to_func_id(s: str) -> str:
    return id_to_lower(str_to_raw_id(s))

def str_to_var_id(s: str) -> str:
    id = id_to_lower(str_to_raw_id(s))
    if id == 'i':
        return 'L'
    return id

def str_to_class_id(s: str) -> str:
    return id_to_camel(str_to_raw_id(s))

def str_to_const_id(s: str) -> str:
    return id_to_upper(str_to_raw_id(s))

def to_str(s: str) -> str:
    if '\n' not in s:
        return f"'{s}'"
    else:
        return f"'''{s}'''"

def to_tuple(t: list) -> str:
    if len(t) == 1:
        return f'{t[0]}'
    else:
        return f"({', '.join(t)})"

__all__ = [
    # 'is_xid_start',
    # 'is_xid_continue',
    # 'str_to_raw_id',
    # 'id_to_lower',
    # 'id_to_camel',
    # 'id_to_upper',
    'str_to_mod_id',
    'str_to_func_id',
    'str_to_var_id',
    'str_to_class_id',
    'str_to_const_id',
    'to_str',
    'to_tuple',
]