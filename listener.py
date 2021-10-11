from sqs_listener import SqsListener
import logging, boto3
from logging.handlers import TimedRotatingFileHandler
import matlab.engine
import converter, compress, s3Uploader


class MyListener(SqsListener):
    def handle_message(self, body, attributes, messages_attributes):
        logger.info(body['file_name'] + '  ' + body['tenant_id'])
        
        eng = matlab.engine.start_matlab()
        eng.estimate_s1s2(body['tenant_id'], body['file_name'], nargout=0)
        eng.quit() 
        converter.conversion(body['tenant_id'], body['file_name']) 
        compress.main(body['tenant_id'], body['file_name'])
        s3Uploader.main(body['tenant_id'], body['file_name'])
        
        
listener = MyListener('av_to_process_dev', error_queue='error-visualization-dev', interval=60, region_name="ap-south-1", message_attribute_names=['All'], attribute_names=['All'])
        
logger = logging.getLogger('sqs_listener')
logger.setLevel(logging.INFO)

logname = "visualization_app.log"
sh = TimedRotatingFileHandler(logname, when="midnight", interval=1)
sh.setLevel(logging.INFO)
sh.suffix = "%Y%m%d"
formatstr = '[%(asctime)s - %(name)s - %(levelname)s]  %(message)s'
formatter = logging.Formatter(formatstr)
sh.setFormatter(formatter)

logger.addHandler(sh)

listener.listen()
