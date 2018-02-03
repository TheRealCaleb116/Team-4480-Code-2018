import wpilib
from networktables import NetworkTables

import multiprocessing

def Start(robotIP):
    c = Checker()
    c.start()
class Checker(object):

    def __init__(self,robotIP):
        NetworkTables.initialize(server=robotIP)
        NetworkTables.addSubTableListener(Check)

    def start():
        NetworkTables.addSubTableListener(Check)

    def Check(self,key,value,isNew):
        pass
