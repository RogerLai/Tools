'''
Created on Jun 19, 2013

@author: roger
'''

from controller import *

urls = [
        (r"/", WebGetIndexHandler),
        (r"/pick", RandomPickHandler),
        (r"/interest_group_expense_history", InterestGroupExpenseHandler),
        ]