'''
Created on Dec 1, 2015

@author: rogerlai
'''

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

def get_all_groups_info():
    sql_statment = 'SELECT group_id, group_name, group_member_count, group_budget, group_expense_total FROM interest_group WHERE is_registered = 1'
    result = helper.select_query(sql_statment, None, True, 'group_id')
    return result