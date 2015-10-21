#!/usr/bin/env Python  
#coding=utf-8
'''
Created on Apr 13, 2015

@author: rogerlai
'''

import tornado.web

from common import process
from common.config import TEMPLATE_PATH, STATIC_HOST, WEB_SERVER_ADDR


loader = tornado.web.template.Loader(TEMPLATE_PATH)

class WebGetIndexHandler(tornado.web.RequestHandler):      
    @staticmethod
    def get_handler(self):            
        param_dict = {}
        param_dict['title'] = u'随机分组'
        param_dict['static_host'] = STATIC_HOST
        param_dict['web_server'] = WEB_SERVER_ADDR
        
        response = loader.load("index.html").generate(params = param_dict)                    
        return response
        
    def get(self):
        self.write(process.process_request(self.request, lambda: WebGetIndexHandler.get_handler(self), 'html')) 