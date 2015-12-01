'''
Created on Apr 13, 2015

@author: rogerlai
'''
import json
import subprocess

from common.config import SERVER_IP
from common.exceptions import IncorrectJsonObjError


def check_if_process_running(process_name, remote_host = None):    
    if remote_host is None or remote_host == SERVER_IP:
        cmd_str = 'ps aux|grep %s' % process_name
    else:
        cmd_str = 'ssh %s "ps aux|grep %s"' % (remote_host, process_name)
    
    result = False
    count = 0
    p = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for _ in p.stdout.readlines():
        count = count + 1
    
    if count >= 3:
        result = True      
        
    p.wait()        
    return result

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
    
def in_clause(id_list):
    try:
        for i in id_list:
            if type(i) not in (int, long):
                return ''
        return str(set(id_list))[5:-2].translate(None,'L')
    except Exception:
        return ''
    
def str_in_clause(str_list):
    try:
        result = ''
        for i in str_list:
            result += '"%s",' % i
        
        result = result[:-1]
        return result
    except Exception:
        return ''      
    
def format_date_to_str(date_obj):
    if date_obj is None:
        return ''
    
    return date_obj.strftime('%m-%d-%Y')