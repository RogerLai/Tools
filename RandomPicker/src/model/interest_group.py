'''
Created on Dec 1, 2015

@author: rogerlai
'''

from common import utils
from db import interest_group_db

def get_all_expense_history():
    response = {}
    response['expense_list'] = []
    lists = interest_group_db.get_all_expense_history()    
    groups = interest_group_db.get_all_groups_info()
    
    for item in lists:
        item['act_date'] = utils.format_date_to_str(item['act_date'])
        
        item_info = {}
        item_info['group_info'] = groups.get(item.get('group_id')) 
        item_info['act_info'] = item
        response['expense_list'].append(item_info)
        
    return response
