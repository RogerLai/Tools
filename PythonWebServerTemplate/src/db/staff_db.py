'''
Created on Oct 21, 2015

@author: rogerlai
'''

from db import helper

def get_all_staff():
    sql_statment = 'SELECT id, name, gender, is_partner, is_admin, is_club_member FROM staff WHERE is_deleted = 0'
    result = helper.select_query(sql_statment, None, True)
    return result