'''
Created on Oct 21, 2015

@author: rogerlai
'''

from common.exceptions import SQLError
from db import helper


def get_all_staff(id_mapping = False):
    sql_statment = 'SELECT id, name, gender, is_partner, is_admin, is_club_member FROM staff WHERE is_deleted = 0'
    
    if id_mapping:
        result = helper.select_query(sql_statment, None, True, 'id')
    else:
        result = helper.select_query(sql_statment, None, True)
    return result

def get_staff_id_mapping():
    sql_statment = 'SELECT staff_id, pair_id FROM staff_id_to_pair_id_mapping WHERE is_valid = 1'
    result = helper.select_query(sql_statment, None, True)
    return result

def get_min_and_max_pair_id():
    sql_statment = 'SELECT MIN(pair_id) AS MIN_ID, MAX(pair_id) AS MAX_ID FROM staff_id_to_pair_id_mapping WHERE is_valid = 1'
    result = helper.select_query(sql_statment, None, True)
    if len(result) == 1:
        return result[0]
    else:
        raise SQLError()