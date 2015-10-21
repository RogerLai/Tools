#!/usr/bin/env Python  
#coding=utf-8
'''
Created on Jun 23, 2013

@author: roger
'''

import tornado
from common.exceptions import ServerError, TokenInvalidError
import traceback
import sys

def format_exception(e):
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

    exception_str = "Traceback (most recent call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]
    return exception_str

def process_request(request, request_handler, resp_type = 'json', log_flag = True):
    try:
        if (log_flag == True):
            __log_request(request)
            
        result = request_handler()
    except TokenInvalidError,e:
        tornado.log.logging.error(format_exception(e))
        return _response(2, request, False, e.error_message)
    except ServerError,e:
        tornado.log.logging.error(format_exception(e))
        return _response(1, request, False, e.error_message)
    except Exception,e:
        tornado.log.logging.error(format_exception(e))
        return _response(1, request, False, e.message)
    else:   # successful
        return _response(0, request, True, result, resp_type)

def _response(status_code, request, success = False, 
              data = "Server request execution failed.",
              resp_type = 'json'):
    if (success == False):
        if (resp_type == 'json'):
            response = {}
            response['status_code'] = status_code
            response['message'] = data
            __log_response(request, response)
        else:
            response = '<html><head><title>出错啦</title></head><body>不好意思，服务器出错啦，请稍后再试</body></html>'
            
        return response
    else:
        if (resp_type == 'json'):
            data['status_code'] = 0
            __log_response(request, data)
              
        return data
        
def __log_request(request):
    user_token = request.headers.get('Http-Token', 'NoToken')    
    request_info = 'Request from: %s %s %s %s' % (request.headers.get('X-Real-IP'), request.method, request.uri, user_token)
    tornado.log.logging.info(request_info)
    
    if (request.method == 'POST'):
        request_body = 'Request body is: %s' % request.body
        tornado.log.logging.info(request_body)

def __log_response(request, body = None):
    user_token = request.headers.get('Http-Token', 'NoToken')        
    response_info = 'Response to : %s %s %s %s' % (request.headers.get('X-Real-IP'), request.method, request.uri, user_token)
    tornado.log.logging.info(response_info)
    
    response_body = 'Response body is: %s' % body
    tornado.log.logging.info(response_body)    
            