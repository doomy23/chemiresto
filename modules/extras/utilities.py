# -*- coding: utf-8 -*-

def get_tuple_value(tuple, key):
    for k, v in tuple:
        if k == key:
            return unicode(v)
        
    return ""