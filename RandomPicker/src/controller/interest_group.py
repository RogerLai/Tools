#coding=utf-8
'''
Created on Dec 1, 2015

@author: rogerlai
'''

import tornado.web

from common import process
from common.config import TEMPLATE_PATH, STATIC_HOST
from model import interest_group


loader = tornado.web.template.Loader(TEMPLATE_PATH)

class InterestGroupExpenseHandler(tornado.web.RequestHandler):
    @staticmethod
    def get_handler(self):
        param_dict = {}
        param_dict['title'] = u'兴趣小组报销' 
        param_dict['group_list'] = interest_group.get_group_lists()
        param_dict['static_host'] = STATIC_HOST
        
        response = loader.load("add_expense.html").generate(params = param_dict)                    
        return response
        
    def get(self):
        self.write(process.process_request(self.request, lambda: InterestGroupExpenseHandler.get_handler(self), 'html'))
    
    @staticmethod
    def post_handler(self):
        param_dict = {}                   
        
        try:
            expense_info = {}
            expense_info['group_id'] = int(self.get_argument('group_id', 0))
            expense_info['act_member_count'] = int(self.get_argument('act_member_count', 0))
            expense_info['act_total_cost'] = int(self.get_argument('act_total_cost', 0))
            expense_info['act_date'] = self.get_argument('act_date')
            
            return_page = 'success.html'
            interest_group.add_new_expense(expense_info)
        except Exception as e:
            param_dict['error_msg'] = e.message
            return_page = 'failure.html' 
        
        param_dict['static_host'] = STATIC_HOST
        response = loader.load(return_page).generate(params = param_dict)                    
        return response
        
    def post(self):
        self.write(process.process_request(self.request, lambda: InterestGroupExpenseHandler.post_handler(self), 'html'))
        
class InterestGroupExpenseHistoryHandler(tornado.web.RequestHandler):
    @staticmethod
    def get_handler(self):
        param_dict = {}
        param_dict['title'] = u'兴趣小组报销'
        param_dict['results'] = interest_group.get_all_expense_history()
        param_dict['static_host'] = STATIC_HOST
        
        response = loader.load("interest_group_expense_list.html").generate(params = param_dict)                    
        return response
        
    def get(self):
        self.write(process.process_request(self.request, lambda: InterestGroupExpenseHistoryHandler.get_handler(self), 'html'))        