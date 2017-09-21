from ConfigParser import ConfigParser


def get_config(key):
    config = ConfigParser()
    # config.read('C:\\Users\\Administrator\\water_sender.ini')
    config.read('/Users/anyisalin/Downloads/water_sender.ini')
    return config.get('config', key)


DB_URL = get_config('db_url')
AES_KEY = get_config('aes_key')
IV = get_config('iv')
ENDPOINT_URL = get_config('endpoint_url')
METRIC_DIR = get_config('metric_dir')
UUID_FILE = get_config('uuid_file')
