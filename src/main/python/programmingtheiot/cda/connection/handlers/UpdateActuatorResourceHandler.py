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
from aiocoap.resource import Resource

from src.main.python.programmingtheiot.common.IDataMessageListener import IDataMessageListener

from src.main.python.programmingtheiot.data.DataUtil import DataUtil
from src.main.python.programmingtheiot.data.ActuatorData import ActuatorData


class UpdateActuatorResourceHandler(Resource):
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        self.dataMsgListener = dataMsgListener
        self.dataUtil = DataUtil()

    async def render_put(self, request):
        try:
            # TODO: validate the request!
            # Check payload
            # Check content-type (should be JSON)
            actuatorCmdData = self.dataUtil.jsonToActuatorData(request.payload)

            return self._createResponse(actuatorCmdData)
        except:
            logging.warning("Failed to validate and convert actuation command.")

        return aiocoap.Message(code=Code.NOT_ACCEPTABLE)

    def _createResponse(self, data: ActuatorData = None):
        responseCode = Code.CHANGED

        actuatorResponseData = self.dataMsgListener.handleActuatorCommandMessage(data)

        # TODO: validate the data and convert to JSON

        # return a Message instance
        jsonData = self.dataUtil.actuatorDataToJson(actuatorResponseData)
        return aiocoap.Message(code=responseCode, payload=jsonData.encode('ascii'))
