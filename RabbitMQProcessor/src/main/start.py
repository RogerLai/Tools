#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Created on Dec 11, 2015

@author: rogerlai
'''

import os
import sys

import pika

from common import utils
from common.config import RABBITMQ_QUEUE_NAME, RABBITMQ_MOVE_TARGET_QUEUE_NAME, RABBITMQ_EXCHANGE_NAME
from common.config import RABBITMQ_URL, MOVE_CRITERIA


reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

"set the python egg cache folder to /tmp, instead of its default folder"
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

def callback(ch, method, properties, body):
    if body is None:
        return
    
    try:
        json_obj = utils.load_json_from_str(body)            
        for criteria_item in MOVE_CRITERIA:
            temp_json_obj = json_obj
            for key_path in criteria_item.get('key_path'):
                temp_json_obj = temp_json_obj.get(key_path)
                if temp_json_obj is None:
                    print 'different path, do not move'
                    return
                
            if temp_json_obj not in criteria_item.get('value_list'):
                print 'different value, do not move'
                return
        
        ch.basic_ack(delivery_tag = method.delivery_tag) 
        channel.basic_publish(exchange = RABBITMQ_EXCHANGE_NAME, routing_key = RABBITMQ_MOVE_TARGET_QUEUE_NAME, body = body, properties = pika.BasicProperties(delivery_mode = 2 ,))
    except Exception as e:
        print 'process failed with exception: %s' % e
        
if __name__ == '__main__': 
    parameters = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters) 
    channel = connection.channel()
     
    try:
        channel.queue_declare(queue = RABBITMQ_QUEUE_NAME, durable = True, passive = True)
    except Exception as e:
        print 'the queue %s does not exist' % e
        
    try:
        channel.queue_declare(queue = RABBITMQ_MOVE_TARGET_QUEUE_NAME, durable = True, passive = True)
    except Exception as e:
        print 'the queue %s does not exist' % e
         
    channel.basic_qos(prefetch_count = 100 ) 
    channel.basic_consume(callback, queue = RABBITMQ_QUEUE_NAME )
    channel.start_consuming()