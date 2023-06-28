import json
import time
from copy import deepcopy

from robots.robot import ServiceRobot, AppRobot
from dbo.cds_dbo import CDSDBOperator
from utils.log_handler import logger as log
from utils.time_handler import HumanDateTime


class CDSAppRobot(AppRobot):
    def __init__(self):
        self.dbo = CDSDBOperator()
        super().__init__()
