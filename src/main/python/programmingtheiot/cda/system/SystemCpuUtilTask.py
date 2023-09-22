import logging
import psutil

from src.main.python.programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
from src.main.python.programmingtheiot.common import ConfigConst


class SystemCpuUtilTask(BaseSystemUtilTask):

    def __init__(self):
        super(SystemCpuUtilTask, self).__init__(name=ConfigConst.CPU_UTIL_NAME, typeID=ConfigConst.CPU_UTIL_TYPE)

    def getTelemetryValue(self) -> float:
        return psutil.cpu_percent()
