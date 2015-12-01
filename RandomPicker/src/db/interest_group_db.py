'''
Created on Dec 1, 2015

@author: rogerlai
'''

import tornado

from common.config import DBPOOL
from common.exceptions import SQLError
from db import helper


GROUP_EXPENSE_FIELDS = 'act_id, group_id, act_member_count, act_total_cost, act_date'

def get_all_expense_history():
    sql_statment = 'SELECT %s FROM interest_group_expense WHERE is_deleted = 0' % GROUP_EXPENSE_FIELDS
    result = helper.select_query(sql_statment, None, True)
    return result

def get_expense_by_group(group_id):
    sql_statment = 'SELECT %s FROM interest_group_expense WHERE is_deleted = 0 AND group_id = ?' % GROUP_EXPENSE_FIELDS
    params = (group_id, )
    result = helper.select_query(sql_statment, params, True)
    return result

def get_expense_by_date(start_date, end_date):
    sql_statment = 'SELECT %s FROM interest_group_expense WHERE is_deleted = 0' % GROUP_EXPENSE_FIELDS
    params = (start_date, end_date)
    result = helper.select_query(sql_statment, params, True)
    return result

def get_all_groups_info(dict_flag = True):
    sql_statment = 'SELECT group_id, group_name, group_member_count, group_budget, group_expense_total FROM interest_group WHERE is_registered = 1'
    sql_key = None
    if dict_flag == True:
        sql_key = 'group_id'
                
    result = helper.select_query(sql_statment, None, True, sql_key)        
    return result

def add_new_expense_record(expense_info):
    try:            
        conn = DBPOOL.connection()
        cursor = conn.cursor()
        cursor.execute("SET AUTOCOMMIT = 0")
                
        sql_stmt = 'INSERT INTO interest_group_expense (group_id, act_member_count, act_total_cost, act_date) VALUES (?, ?, ?, ?)'
        params = (expense_info.get('group_id'), expense_info.get('act_member_count'), 
                  expense_info.get('act_total_cost'), expense_info.get('act_date'))
        
        cursor.execute(sql_stmt, params)        
        comment_id = cursor.lastrowid
        
        conn.commit()
        
        cursor.execute("SET AUTOCOMMIT = 1")
        return comment_id
    except Exception, e:
        conn.rollback()  
        tornado.log.logging.error(e)
        raise SQLError
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()