#coding=utf-8
'''
Created on Oct 21, 2015

@author: rogerlai
'''

import random
from random import randint

from db import staff_db

def get_pair_pick_result():
    result = []
    staffs = staff_db.get_all_staff(True)
    pairs = staff_db.get_staff_id_mapping()
    min_id = 1
    max_id = 5
    id_occupied = {}
    for item in pairs:
        while True:
            random_value = randint(min_id, max_id)
            if random_value != item['pair_id'] and id_occupied.get(random_value) is None:
                item['gift_id'] = random_value
                item['staff_name'] = staffs.get(item['staff_id'], {}).get('name')
                id_occupied[random_value] = True
                break
            
        result.append(item)
    
    result.sort(key=lambda x: x['gift_id'], reverse = False) 
    return result

def get_pick_result(group_count, club_member_dispatch_flag = False, gender_dispatch_flag = False):
    result = {}
    
    all_staff = staff_db.get_all_staff()
    for staff in all_staff:
        v = random.random()                
        if club_member_dispatch_flag == True and staff['is_club_member'] == 1:
            v = v + 1000
            
        if staff['is_partner'] == 1:
            v = v + 100
            
        if gender_dispatch_flag == True and staff['gender'] == 2:
            v = v + 10
            
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
    result = get_pick_result(4, True, True)
    print result