'''
Created on Dec 11, 2015

@author: rogerlai
'''

RABBITMQ_USER_NAME = 'root'
RABBITMQ_PASSWORD = 'bigbang!'
RABBITMQ_HOST = '112.124.70.25'
RABBITMQ_PORT = 5672
RABBITMQ_URL = 'amqp://%s:%s@%s:%s/' % (RABBITMQ_USER_NAME, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_PORT) + '%2F'
RABBITMQ_QUEUE_NAME = 'file_preconversion_fail_queue'
RABBITMQ_MOVE_TARGET_QUEUE_NAME = 'file_preconversion_fail_queue_temp'
RABBITMQ_EXCHANGE_NAME = 'job_queues_exchange'

WRITE_TO_FILE = True
LOCAL_FILE_PATH = '/Users/rogerlai/Documents/logs/rabbit_mq.log'

MOVE_CRITERIA = [{
    'key_path': ['convert_kinds', 'image_128', 'format'],
    'value_list': ['jpg']
}]