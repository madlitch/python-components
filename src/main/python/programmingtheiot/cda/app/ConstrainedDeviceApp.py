import logging

from time import sleep

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil
from src.main.python.programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager

logging.basicConfig(format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s', level = logging.DEBUG)

class ConstrainedDeviceApp():
    def __init__(self):
        logging.info("Initializing CDA...")

        self.dataMgr = DeviceDataManager()

    def startApp(self):
        logging.info("Starting CDA...")

        self.dataMgr.startManager()

        logging.info("CDA started.")

    def stopApp(self, code: int):
        logging.info("CDA stopping...")

        self.dataMgr.stopManager()

        logging.info("CDA stopped with exit code %s.", str(code))

def main():
    cda = ConstrainedDeviceApp()
    cda.startApp()

    runForever = ConfigUtil().getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.RUN_FOREVER_KEY)

    if runForever:
        while (True):
            sleep(5)

    else:
        # TODO: Make the '65' value configurable
        sleep(65)
        cda.stopApp(0)

if __name__ == '__main__':
    main()