#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.data.SensorData import SensorData
from src.main.python.programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet


class BaseSensorSimTask():
    """
    Shell representation of class for student implementation.

    """

    DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
    DEFAULT_MAX_VAL = 100.0

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE,
                 dataSet: SensorDataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
        self.dataSet = dataSet
        self.name = name
        self.typeID = typeID
        self.dataSetIndex = 0
        self.useRandomizer = False

        self.latestSensorData = None

        if not self.dataSet:
            self.useRandomizer = True
            self.minVal = minVal
            self.maxVal = maxVal

    def generateTelemetry(self) -> SensorData:
        sensorData = SensorData(typeID=self.typeID, name=self.name)
        sensorVal = ConfigConst.DEFAULT_VAL

        if self.useRandomizer:
            sensorVal = random.uniform(self.minVal, self.maxVal)
        else:
            sensorVal = self.dataSet.getDataEntry(index=self.dataSetIndex)
            self.dataSetIndex = self.dataSetIndex + 1

            if self.dataSetIndex >= self.dataSet.getDataEntryCount() - 1:
                self.dataSetIndex = 0

        sensorData.setValue(sensorVal)

        self.latestSensorData = sensorData

        return self.latestSensorData

    def getTelemetryValue(self) -> float:
        if not self.latestSensorData:
            self.generateTelemetry()

        return self.latestSensorData.getValue()

    def getLatestTelemetry(self) -> SensorData:
        """
        This can return the current SensorData instance or a copy.
        """
        pass

    def getName(self) -> str:
        pass

    def getTypeID(self) -> int:
        pass
