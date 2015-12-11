'''
Created on Dec 11, 2015

@author: rogerlai
'''

RABBITMQ_USER_NAME = 'root'
RABBITMQ_PASSWORD = 'bigbang!'
RABBITMQ_HOST = 'file_conversion_fail_queue'
RABBITMQ_PORT = 5637
RABBITMQ_URL = 'amqp://%s:%s@%s:%s/' % (RABBITMQ_USER_NAME, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT) + '%2F'
RABBITMQ_QUEUE_NAME = 'file_preconversion_fail_queue'
RABBITMQ_MOVE_TARGET_QUEUE_NAME = 'file_preconversion_fail_queue_temp'
RABBITMQ_EXCHANGE_NAME = 'job_queues_exchange'

MOVE_CRITERIA = [{'key_path':[''], 'value_list':[]}]