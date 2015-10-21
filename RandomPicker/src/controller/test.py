'''
Created on Apr 13, 2015

@author: rogerlai
'''

import tornado.web

from common import process


class TestHandler(tornado.web.RequestHandler):
    @staticmethod
    def get_handler(self):
        response = {}
        response['text'] = 'hello'
        return response
        
    def get(self):
        self.write(process.process_request(self.request, lambda: TestHandler.get_handler(self)))