# Source Generated with Decompyle++
# File: helpers.pyc (Python 2.7)

import os
import re
import json
import uuid
from fuck_water_sender.logger import logger
from fuck_water_sender import constants as C
FILEPATTERN = re.compile('.*Par2(?P<date>[0-9\\-]+).txt')


class FuckingFileParser(object):

    def __init__(self, filename):
        self._file = open(filename, 'r')
        self.title = self.parse(self._file.readline())

    @staticmethod
    def parse(line):
        return line.strip('\n').strip('\r').split('\t')[0:6]

    @property
    def date(self):
        return FILEPATTERN.match(self._file.name).groupdict().get('date')

    def readlines(self):
        ret = []
        for line in self._file.readlines():
            if not line.strip('\r').strip('\n'):
                continue
            new_line = self.parse(line)
            new_line.insert(0, self.date)
            ret.append(new_line)

        return ret

    def close(self):
        self._file.close()


def generate_uuid():
    with open(C.UUID_FILE, 'w') as f:
        logger.info('generate uuid')
        f.write(json.dumps({
            'uuid': str(uuid.uuid4())}))


def get_uuid():
    if not os.path.isfile(C.UUID_FILE):
        generate_uuid()
    with open(C.UUID_FILE, 'r') as f:
        u = json.load(f)
    return u['uuid']
