import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst


class BaseSystemUtilTask():

    def __init__(self, name=ConfigConst.NOT_SET, typeID=ConfigConst.DEFAULT_SENSOR_TYPE):
        self.name = name
        self.typeID = typeID

    def getName(self) -> str:
        return self.name

    def getTypeID(self) -> int:
        return self.typeID

    def getTelemetryValue(self) -> float:
        pass
