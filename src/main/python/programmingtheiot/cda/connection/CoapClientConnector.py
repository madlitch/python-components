#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import socket
import traceback
import asyncio

from aiocoap import *

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.common.ConfigUtil import ConfigUtil

from src.main.python.programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from src.main.python.programmingtheiot.common.IDataMessageListener import IDataMessageListener
from src.main.python.programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient

from src.main.python.programmingtheiot.data.DataUtil import DataUtil


class CoapClientConnector(IRequestResponseClient):
    """
    Shell representation of class for student implementation.

    """

    def __init__(self, dataMsgListener: IDataMessageListener = None):
        self.config = ConfigUtil()
        self.dataMsgListener = dataMsgListener
        self.enableConfirmedMsgs = False
        self.coapClient = None

        self.observeRequests = {}

        self.host = self.config.getProperty(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.HOST_KEY,
                                            ConfigConst.DEFAULT_HOST)
        self.port = self.config.getInteger(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.PORT_KEY,
                                           ConfigConst.DEFAULT_COAP_PORT)
        self.uriPath = "coap://" + self.host + ":" + str(self.port) + "/"

        logging.info('\tHost:Port: %s:%s', self.host, str(self.port))

        self.includeDebugLogDetail = True

        try:
            tmpHost = socket.gethostbyname(self.host)

            if tmpHost:
                self.host = tmpHost
                self._initClient()
            else:
                logging.error("Can't resolve host: " + self.host)

        except socket.gaierror:
            logging.info("Failed to resolve host: " + self.host)

    def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("Discovering remote resources...")

        return self.sendGetRequest(resource=None, name='.well-known/core', enableCON=False, timeout=timeout)

    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False,
                          timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)

            logging.info("Issuing Async DELETE to path: " + resourcePath)

            asyncio.get_event_loop().run_until_complete(
                self._handleDeleteRequest(resourcePath=resourcePath, enableCON=enableCON))
        else:
            logging.warning("Can't issue Async DELETE - no path or path list provided.")

    def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False,
                       timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)

            logging.info("Issuing Async GET to path: " + resourcePath)

            asyncio.get_event_loop().run_until_complete(
                self._handleGetRequest(resourcePath=resourcePath, enableCON=enableCON))
        else:
            logging.warning("Can't issue Async GET - no path or path list provided.")

    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False,
                        payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)

            logging.info("Issuing Async POST to path: " + resourcePath)

            asyncio.get_event_loop().run_until_complete(
                self._handlePostRequest(resourcePath=resourcePath, payload=payload, enableCON=enableCON))
        else:
            logging.warning("Can't issue Async POST - no path or path list provided.")

    def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False,
                       payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)

            logging.info("Issuing Async PUT to path: " + resourcePath)

            asyncio.get_event_loop().run_until_complete(
                self._handlePutRequest(resourcePath=resourcePath, payload=payload, enableCON=enableCON))
        else:
            logging.warning("Can't issue Async PUT - no path or path list provided.")

    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        if listener:
            self.dataMsgListener = listener

    def startObserver(self, resource: ResourceNameEnum = None, name: str = None,
                      ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)

            if resourcePath in self.observeRequests:
                logging.warning("Already observing resource %s. Ignoring start observe request.", resourcePath)
                return

            asyncio.get_event_loop().run_until_complete( \
                asyncio.ensure_future(self._handleStartObserveRequest(resourcePath)))
        else:
            logging.warning("Can't issue Async OBSERVE - GET - no path or path list provided.")

    def stopObserver(self, resource: ResourceNameEnum = None, name: str = None,
                     timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)

            if not resourcePath in self.observeRequests:
                logging.warning("Resource %s not being observed. Ignoring stop observe request.", resourcePath)
                return

            asyncio.get_event_loop().run_until_complete( \
                self._handleStopObserveRequest(resourcePath))
        else:
            logging.warning("Can't cancel OBSERVE - GET - no path provided.")

    def _initClient(self):
        asyncio.get_event_loop().run_until_complete(self._initClientContext())

    async def _initClientContext(self):
        try:
            logging.info("Creating CoAP client for URI path: " + self.uriPath)

            self.coapClient = await Context.create_client_context()

            logging.info('Client context created. Will invoke resources at: ' + self.uriPath)
        except Exception as e:
            # obviously, this is a critical failure - you may want to handle this differently
            logging.error("Failed to create CoAP client to URI path: " + self.uriPath)
        # traceback.print_exception(type(e), e, e.__traceback__)

    def _createResourcePath(self, resource: ResourceNameEnum = None, name: str = None):
        resourcePath = ""
        hasResource = False

        if resource:
            resourcePath = resourcePath + resource.value
            hasResource = True

        if name:
            if hasResource:
                resourcePath = resourcePath + '/'

            resourcePath = resourcePath + name

        return resourcePath

    async def _handleGetRequest(self, resourcePath: str = None, enableCON: bool = False):
        try:
            msgType = NON

            if enableCON:
                msgType = CON

            msg = Message(mtype=msgType, code=Code.GET, uri=resourcePath)
            req = self.coapClient.request(msg)
            responseData = await req.response

            self._onGetResponse(responseData)
        except Exception as e:
            # TODO: for debugging, you may want to optionally include the stack trace, as shown
            logging.warning("Failed to process GET request for path: " + self.uriPath)
        # traceback.print_exception(type(e), e, e.__traceback__)

    def _onGetResponse(self, response):
        if not response:
            logging.warning('Async GET response invalid. Ignoring.')
            return

        logging.info('Async GET response received.')

        jsonData = response.payload.decode("utf-8")

        if len(response.requested_path) >= 2:
            dataType = response.requested_path[2]

            if dataType == ConfigConst.ACTUATOR_CMD:
                # TODO: convert payload to ActuatorData and verify!
                logging.info("ActuatorData received: %s", jsonData)

                try:
                    ad = DataUtil().jsonToActuatorData(jsonData)

                    if self.dataMsgListener:
                        self.dataMsgListener.handleActuatorCommandMessage(ad)
                except:
                    logging.warning("Failed to decode actuator data. Ignoring: %s", jsonData)
                    return
            else:
                logging.info("Response data received. Payload: %s", jsonData)
        else:
            logging.info("Response data received. Payload: %s", jsonData)

    async def _handlePutRequest(self, resourcePath: str = None, payload: str = None, enableCON: bool = False):
        try:
            msgType = NON

            if enableCON:
                msgType = CON

            payloadBytes = b''

            # decide which encoding to use - can also load from config
            if payload:
                payloadBytes = payload.encode('utf-8')

            msg = Message(mtype=msgType, payload=payloadBytes, code=Code.PUT, uri=resourcePath)
            req = self.coapClient.request(msg)
            responseData = await req.response

            self._onPutResponse(responseData)

        except Exception as e:
            # TODO: for debugging, you may want to optionally include the stack trace, as shown
            logging.warning("Failed to process PUT request for path: " + resourcePath)
        # traceback.print_exception(type(e), e, e.__traceback__)

    def _onPutResponse(self, response):
        if not response:
            logging.warning('PUT response invalid. Ignoring.')
            return

        logging.info('PUT response received: %s', response.payload)

    async def _handlePostRequest(self, resourcePath: str = None, payload: str = None, enableCON: bool = False):
        try:
            msgType = NON

            if enableCON:
                msgType = CON

            payloadBytes = b''

            # decide which encoding to use - can also load from config
            if payload:
                payloadBytes = payload.encode('utf-8')

            msg = Message(mtype=msgType, payload=payloadBytes, code=Code.POST, uri=resourcePath)
            req = self.coapClient.request(msg)
            responseData = await req.response

            self._onPostResponse(responseData)

        except Exception as e:
            # TODO: for debugging, you may want to optionally include the stack trace, as shown
            logging.warning("Failed to process POST request for path: " + resourcePath)
        # traceback.print_exception(type(e), e, e.__traceback__)

    def _onPostResponse(self, response):
        if not response:
            logging.warning('POST response invalid. Ignoring.')
            return

        logging.info('POST response received: %s', response.payload)

    async def _handleDeleteRequest(self, resourcePath: str = None, enableCON: bool = False):
        try:
            msgType = NON

            if enableCON:
                msgType = CON

            msg = Message(mtype=msgType, code=Code.DELETE, uri=resourcePath)
            req = self.coapClient.request(msg)
            responseData = await req.response

            self._onDeleteResponse(responseData)

        except Exception as e:
            # TODO: for debugging, you may want to optionally include the stack trace, as shown
            logging.warning("Failed to process DELETE request for path: " + resourcePath)
        # traceback.print_exception(type(e), e, e.__traceback__)

    def _onDeleteResponse(self, response):
        if not response:
            logging.warning('DELETE response invalid. Ignoring.')
            return

        logging.info('DELETE response received: %s', response.payload)

    async def _handleStartObserveRequest(self, resourcePath: str = None):
        logging.info('Handle start observe invoked. Waiting for each input: ' + resourcePath)

        msg = Message(code=Code.GET, uri=resourcePath, observe=0)
        req = self.clientContext.request(msg)

        self.observeRequests[resourcePath] = req

        try:
            responseData = await req.response

            # TODO: validate response first
            self._onGetResponse(responseData)

            async for responseData in req.observation:
                # TODO: validate response first
                self._onGetResponse(responseData)

                req.observation.cancel()
                break

        except Exception as e:
            # TODO: log warning and possibly stack trace, then be sure to stop observing...
            logging.warning("Failed to execute OBSERVE - GET. Recovering...")
        # traceback.print_exception(type(e), e, e.__traceback__)

    async def _handleStopObserveRequest(self, resourcePath: str = None, ignoreErr: bool = False):
        if resourcePath in self.observeRequests:
            logging.info('Handle stop observe invoked: ' + resourcePath)

            try:
                observeRequest = self.observeRequests[resourcePath]
                observeRequest.observation.cancel()
            except Exception as e:
                if not ignoreErr:
                    logging.warning("Failed to cancel OBSERVE - GET: " + resourcePath)

            try:
                del self.observeRequests[resourcePath]
            except Exception as e:
                if not ignoreErr:
                    logging.warning("Failed to remove observable from list: " + resourcePath)

        else:
            logging.warning('Resource not currently under observation. Ignoring: ' + resourcePath)

    class HandleActuatorEvent():
        def __init__(self, \
                     listener: IDataMessageListener = None, \
                     resourcePath: str = None, \
                     requests=None):

            self.listener = listener
            self.resourcePath = resourcePath
            self.observeRequests = requests

        def handleActuatorResponse(self, response):
            if response:
                jsonData = response.payload

                self.observeRequests[self.resourcePath] = response

                logging.info("Received actuator command response to resource %s: %s", self.resourcePath, jsonData)

                if self.listener:
                    try:
                        data = DataUtil().jsonToActuatorData(jsonData=jsonData)
                        self.listener.handleActuatorCommandMessage(data=data)
                    except:
                        logging.warning("Failed to decode actuator data for resource %s. Ignoring: %s",
                                        self.resourcePath, jsonData)
