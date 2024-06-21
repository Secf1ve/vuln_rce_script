from payloads.pluginmanager import Vuln_Scan

class Plugin1(Vuln_Scan):
    def __init__(self):
        pass
    #实现接入点的接口
    def Start(self):
        print("I am plugin1!")

class Plugin2(Vuln_Scan):
    def __init__(self):
        pass
    #实现接入点的接口
    def Start(self):
        print("I am plugin2!")