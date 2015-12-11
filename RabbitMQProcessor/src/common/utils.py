'''
Created on Apr 13, 2015

@author: rogerlai
'''
import json

from common.exceptions import IncorrectJsonObjError

def _decode_list(lst):
    newlist = []
    for i in lst:
        if isinstance(i, unicode):
            i = i.encode('utf-8')
        elif isinstance(i, list):
            i = _decode_list(i)
        newlist.append(i)
    return newlist

def _decode_dict(dct):
    newdict = {}
    for k, v in dct.iteritems():
        if isinstance(k, unicode):
            k = k.encode('utf-8')
        if isinstance(v, unicode):
            v = v.encode('utf-8')
        elif isinstance(v, list):
            v = _decode_list(v)
        newdict[k] = v
    return newdict

def load_json_from_str(s):
    try:
        result = json.loads(s, object_hook=_decode_dict)
        return result 
    except Exception:
        raise IncorrectJsonObjError 