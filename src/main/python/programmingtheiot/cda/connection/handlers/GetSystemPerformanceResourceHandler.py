#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging

import aiocoap

from aiocoap import Code
from aiocoap.resource import ObservableResource

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil
from src.main.python.programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener

from src.main.python.programmingtheiot.data.DataUtil import DataUtil
from src.main.python.programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from src.main.python.programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener


class GetSystemPerformanceResourceHandler(ObservableResource, ISystemPerformanceDataListener):
    def __init__(self):
        super().__init__()

        self.pollCycles = \
            ConfigUtil().getInteger( \
                section=ConfigConst.CONSTRAINED_DEVICE, \
                key=ConfigConst.POLL_CYCLES_KEY, \
                defaultVal=ConfigConst.DEFAULT_POLL_CYCLES)

        self.dataUtil = DataUtil()
        self.sysPerfData = None

        # for testing
        self.payload = "GetSysPerfData"

    async def render_get(self, request):
        responseCode = Code.CONTENT  # TODO: change to appropriate value

        if not self.sysPerfData:
            self.sysPerfData = SystemPerformanceData()

        jsonData = self.dataUtil.systemPerformanceDataToJson(self.sysPerfData)

        return aiocoap.Message(code=responseCode, payload=jsonData.encode('ascii'))
