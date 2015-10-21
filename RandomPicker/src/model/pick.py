#coding=utf-8
'''
Created on Oct 21, 2015

@author: rogerlai
'''

import random

from db import staff_db


def get_pick_result(group_count, club_member_dispatch_flag = False):
    result = {}
    
    all_staff = staff_db.get_all_staff()
    for staff in all_staff:
        v = random.random()
        if club_member_dispatch_flag == True and staff['is_club_member'] == 1:
            v = v + 1
        staff['random_value'] = v 
    
    # sort the staff
    all_staff.sort(key=lambda x: x['random_value'], reverse = True)
        
    result['group_names'] = []
    result['group_count'] = group_count
    for i in range(group_count):
        group_name = u'第%s组' % (i + 1)
        result['group_names'].append(group_name)
    
    index = 0
    max_row = 0
    result['matrix'] = {}
    for staff in all_staff:
        if result['matrix'].get(index) is None:
            result['matrix'][index] = []
            
        result['matrix'][index].append(staff['name'])
        index = index + 1
        if index == group_count:
            max_row = max_row + 1
            index = 0
    
    if index > 0:
        max_row = max_row + 1
        while index < group_count:
            result['matrix'][index].append(None)
            index = index + 1
        
    result['max_row'] = max_row  
    return result 

if __name__ == "__main__":
    result = get_pick_result(4, True)
    print result