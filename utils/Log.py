import datetime
import logging

def log(props, content):
    # GetLogger
    logger = logging.getLogger('SastSearch')
    
    # Retrieve Data
    time = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ']'
    user = ''
    if props['login']['success'] == '0':
        user = '<Anonymous>'
    else:
        user = '<' + props['login']['email'] + '>'
    
    
    
    logger.info("%s %s %s" % (time, user, content))
