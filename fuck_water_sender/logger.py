import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s [%(processName)s] [%(threadName)s] - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
