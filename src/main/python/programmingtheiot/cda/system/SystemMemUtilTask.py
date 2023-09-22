import logging
import psutil

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask


class SystemMemUtilTask(BaseSystemUtilTask):

    def __init__(self):
        super(SystemMemUtilTask, self).__init__(name=ConfigConst.MEM_UTIL_NAME, typeID=ConfigConst.MEM_UTIL_TYPE)

    def getTelemetryValue(self) -> float:
        return psutil.virtual_memory().percent
