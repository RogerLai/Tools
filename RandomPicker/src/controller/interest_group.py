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
        param_dict['results'] = interest_group.get_all_expense_history()
        param_dict['static_host'] = STATIC_HOST
        
        response = loader.load("interest_group_expense_list.html").generate(params = param_dict)                    
        return response
        
    def get(self):
        self.write(process.process_request(self.request, lambda: InterestGroupExpenseHandler.get_handler(self), 'html'))
    
    @staticmethod
    def post_handler(self):
        param_dict = {}            
        param_dict['results'] = []
        param_dict['static_host'] = STATIC_HOST
        
        response = loader.load("pick_result.html").generate(params = param_dict)                    
        return response
        
    def post(self):
        self.write(process.process_request(self.request, lambda: InterestGroupExpenseHandler.post_handler(self), 'html'))