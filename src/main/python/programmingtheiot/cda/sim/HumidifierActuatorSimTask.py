#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
#

import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst

from src.main.python.programmingtheiot.data.ActuatorData import ActuatorData
from src.main.python.programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask


class HumidifierActuatorSimTask(BaseActuatorSimTask):
    def __init__(self):
        super( \
            HumidifierActuatorSimTask, self).__init__( \
            name=ConfigConst.HUMIDIFIER_ACTUATOR_NAME, \
            typeID=ConfigConst.HUMIDIFIER_ACTUATOR_TYPE, \
            simpleName="HUMIDIFIER")
