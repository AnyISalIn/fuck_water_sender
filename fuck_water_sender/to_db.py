import os
import re
import time
import calendar
import traceback

from datetime import datetime

from fuck_water_sender.logger import logger
from fuck_water_sender import constants as C
from fuck_water_sender.helpers import FuckingFileParser
from fuck_water_sender.db import Metric, session, Base, engine


TITLE = ['timestamp', 'COD', 'NH3', 'TP', 'TN', 'SS']
FILEPATTERN = re.compile(r'Par2[0-9]{4}-[0-9\-]+.txt')
parsed_files = {}


def get_files(dir):
    files = os.listdir(dir)
    for file in files:
        if FILEPATTERN.match(file):
            yield os.path.join(dir, file)


def read_data(filename):
    f = FuckingFileParser(filename)
    for line in f.readlines():
        date, time = line[:2]
        timestamp = calendar.timegm(datetime.strptime('{} {}'.format(
            date, time), '%Y-%m-%d %H:%M').utctimetuple())
        new_line = line[2:]
        new_line.insert(0, timestamp)
        yield dict(zip(TITLE, new_line))
    f.close()


def process_file(filename):
    for item in read_data(filename):
        timestamp = item['timestamp']
        if session.query(Metric).filter_by(TIMESTAMP=timestamp).first():
            logger.info('Metric {} is exists continue'.format(timestamp))
            continue
        try:
            item = {k: float(v) for k, v in item.items() if k != 'timestamp'}
            item['TIMESTAMP'] = timestamp
            m = Metric(**item)
            logger.info(m)
            session.add(m)
            session.commit()
        except:
            logger.warning(traceback.format_exc())
            continue


def main():
    Base.metadata.create_all(engine)
    while True:
        files = list(get_files(C.METRIC_DIR))
        for file in files:
            file_size = os.stat(file).st_size
            if file not in parsed_files:
                parsed_files[file] = dict(last_size=file_size)
                process_file(file)
            elif file_size > parsed_files[file]['last_size']:
                parsed_files[file]['last_size'] = file_size
                process_file(file)
        time.sleep(5)
