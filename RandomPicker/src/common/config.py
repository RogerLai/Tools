#!/usr/bin/env Python  
#coding=utf-8
'''
Created on Apr 13, 2015

@author: rogerlai
'''

import os

from DBUtils.PooledDB import PooledDB
import oursql


# where the service is deployed
SERVER_IP = '121.40.149.171'
WEB_SERVER_ADDR = 'http://121.40.149.171:8088'
STATIC_HOST = 'http://121.40.149.171:26/static'

HTTP_REQUEST_TIMEOUT_IN_SECONDS = 5

# DB information
DB_HOST = '121.40.149.171'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'bigbang!' 
DB_SCHEMA = 'fangcloud'
MAX_CONN = 10

DB_SREVER = DB_HOST + ':' + str(DB_PORT)

DBPOOL = PooledDB(oursql,
                         maxconnections = MAX_CONN,
                         blocking = 1,
                         host = DB_HOST,
                         port = DB_PORT,
                         user = DB_USER,
                         passwd = DB_PASSWORD,
                         db = DB_SCHEMA,
                         use_unicode = False)

#convert a relative path to absolute
def resolve_path(relative_path, absolute_path = None):
    # if absolute path wasn't specified, use current dir instead.
    if not absolute_path:
        absolute_path = os.path.abspath(os.path.dirname(__file__))
    
    while (relative_path.startswith('../')):
        absolute_path = os.path.dirname(absolute_path)
        relative_path = relative_path[3:] 

    if (not relative_path.startswith('/')):
        relative_path = '/' + relative_path

    return absolute_path + relative_path

TEMPLATE_PATH = resolve_path('../templates')