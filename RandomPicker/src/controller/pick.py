'''
Created on Aug 9, 2015

@author: rogerlai
'''
import tornado.web

from common import process
from common.config import TEMPLATE_PATH, STATIC_HOST
from model import pick


loader = tornado.web.template.Loader(TEMPLATE_PATH)

class RandomPickHandler(tornado.web.RequestHandler):
    @staticmethod
    def get_handler(self):
        param_dict = {}        
        group_count = int(self.get_argument('group_count', 0))
        club_member_dispatch_flag = False
        if self.get_argument('club_member_dispatch_flag', 'false') == 'true':
            club_member_dispatch_flag = True
            
        gender_dispatch_flag = False
        if self.get_argument('gender_dispatch_flag', 'false') == 'true':
            gender_dispatch_flag = True
            
        param_dict['results'] = pick.get_pick_result(group_count, club_member_dispatch_flag, gender_dispatch_flag)
        param_dict['static_host'] = STATIC_HOST
        
        response = loader.load("pick_result.html").generate(params = param_dict)                    
        return response
        
    def get(self):
        self.write(process.process_request(self.request, lambda: RandomPickHandler.get_handler(self), 'html'))