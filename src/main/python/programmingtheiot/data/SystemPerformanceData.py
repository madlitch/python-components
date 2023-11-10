#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.data.BaseIotData import BaseIotData

class SystemPerformanceData(BaseIotData):
	def __init__(self, typeID: int = ConfigConst.SYSTEM_PERF_TYPE, name=ConfigConst.SYSTEM_PERF_NAME, d=None):
		super(SystemPerformanceData, self).__init__(name=name, typeID=typeID, d=d)
		self.cpuUtil = ConfigConst.DEFAULT_VAL
		self.memUtil = ConfigConst.DEFAULT_VAL
		self.diskUtil = ConfigConst.DEFAULT_VAL
		self.stateData = ""
		self.isResponse = False

	def getCpuUtilization(self):
		self.updateTimeStamp()
		return self.cpuUtil

	def setCpuUtilization(self, val: float):
		self.updateTimeStamp()
		self.cpuUtil = val

	def getMemoryUtilization(self):
		self.updateTimeStamp()
		return self.memUtil

	def setMemoryUtilization(self, val: float):
		self.updateTimeStamp()
		self.memUtil = val

	def getDiskUtilization(self):
		self.updateTimeStamp()
		return self.diskUtil

	def setDiskUtilization(self, val: float):
		self.updateTimeStamp()
		self.diskUtil = val

	def getCommand(self) -> int:
		return self.command

	def getStateData(self) -> str:
		return self.stateData

	def getValue(self) -> float:
		return self.value

	def isResponseFlagEnabled(self) -> bool:
		return self.isResponse

	def setCommand(self, command: int):
		self.command = command
		self.updateTimeStamp()

	def setAsResponse(self):
		self.isResponse = True
		self.updateTimeStamp()

	def setStateData(self, stateData: str):
		if stateData:
			self.stateData = stateData
			self.updateTimeStamp()

	def setValue(self, val: float):
		self.value = val
		self.updateTimeStamp()

	def _handleUpdateData(self, data):
		if data and isinstance(data, SystemPerformanceData):
			self.cpuUtil = data.cpuUtil
			self.memUtil = data.memUtil
			self.diskUtil = data.diskUtil
			self.isResponse = data.isResponseFlagEnabled()
