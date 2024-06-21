import sys
from payloads.pluginmanager import PluginManager
from payloads.pluginmanager import __ALLMODEL__

if __name__ == '__main__':
    #加载所有插件
    #PluginManager.LoadAllPlugin()

    plugins=  PluginManager.GetPluginByName("Vuln_Scan")
    print(plugins)
    for item in plugins:
        #调用接入点的公共接口
        item.Start()

    '''
    #遍历所有接入点下的所有插件
    for SingleModel in __ALLMODEL__:
    plugins = SingleModel.GetPluginObject()
    print(plugins)
    for item in plugins:
        #调用接入点的公共接口
        item.Start()
    '''



