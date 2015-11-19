'''
Created on Jun 5, 2013

@author: roger
'''

import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

"set the python egg cache folder to /tmp, instead of its default folder"
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

import tornado.options
from common import config
from server_urls import urls

application = tornado.web.Application(urls)

if __name__ == "__main__":
    tornado.options.parse_config_file(config.resolve_path("../../cfg/log.conf"))
    
    if (len(sys.argv) == 2):
        port = int(sys.argv[1].split('=')[1])
    else:
        port = 8088
    
    application.listen(port)
    
    tornado.ioloop.IOLoop.instance().start()