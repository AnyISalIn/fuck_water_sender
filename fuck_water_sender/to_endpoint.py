from time import sleep
from threading import Event
from datetime import datetime
from fuck_water_sender.logger import logger
from fuck_water_sender import constants as C
from fuck_water_sender.helpers import get_uuid
from fuck_water_sender.db import session, Metric
from fuck_water_sender.security import WaterCipher
from fuck_water_sender.db import session, engine, Metric, Base

import copy
import json
import requests
import calendar

event = Event()


METRIC_KEY = ['TIMESTAMP', 'COD', 'NH3', 'TP', 'TN', 'SS']


def read_data():
    items = session.query(Metric).filter_by(sended=False).all()
    if not items:
        sleep(5)
    for item in items:
        try:
            logger.info('process metric {}'.format(item))
            data = {k: v for k, v in copy.deepcopy(
                item.__dict__.items()) if k in METRIC_KEY}
            if not data:
                continue
        except Exception:
            logger.warning(traceback.format_exc())
        yield data, item


def main():
    w = WaterCipher()
    while not event.is_set():
        for data, item in read_data():
            data['UUID'] = get_uuid()
            enc_data = w.encrypt(json.dumps(data))
            res = requests.post(
                C.ENDPOINT_URL, data=enc_data)
            if res.status_code > 400:
                logger.warning('some error {}'.format(res.text))
                sleep(0.2)
            else:
                logger.info('{} send success'.format(item))
                item.sended = True
                session.add(item)
                session.commit()
