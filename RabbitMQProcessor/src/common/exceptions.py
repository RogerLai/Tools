#!/usr/bin/env Python  
#coding=utf-8
'''
Created on Jun 23, 2013

@author: roger
'''

class ErrorMessage:
    token_invalid = u'没有Token，或者Token已经无效，请重新登录'
    invalid_login = u'用户名和密码不匹配，请确认后重新尝试'
    incorrect_json_format = u'不是有效的JSON格式'
    db_query_execution_error = u'数据库操作失败，请稍后重试'

class ServerError(Exception):
    # define basic emma exception
    def __init__(self, error_message):
        Exception.__init__(self, error_message)
        self.error_message = error_message

class TokenInvalidError(ServerError):
    def __init__(self, error_message = ErrorMessage.token_invalid):
        ServerError.__init__(self, error_message)    
        
class InvalidLoginError(ServerError):
    def __init__(self, error_message = ErrorMessage.invalid_login):
        ServerError.__init__(self, error_message)                        
        
class IncorrectJsonObjError(ServerError):
    def __init__(self, error_message = ErrorMessage.incorrect_json_format):
        ServerError.__init__(self, error_message)
        
class SQLError(ServerError):
    def __init__(self, error_message = ErrorMessage.db_query_execution_error):
        ServerError.__init__(self, error_message)        