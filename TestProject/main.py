import os
import time

from rich.console import Console

c = Console()  # 实例化控制台输出


class plugin:

    def __init__(self):
        self.pluginFile = []  # 存储插件文件名称

    def loadPlugins(self):
        # 在plugins中获取插件文件
        try:
            for pluginName in os.listdir("./plugins/"):
                if pluginName.endswith('.py') or not pluginName.startswith("_"):
                    self.configPlugins(pluginName)
                    self.pluginFile.append(str(pluginName))  # 将文件名称添加到数组
        except Exception as re:
            pass
        c.log("[Notice]：", "已完成所有插件加载", style="#a4ff8f")
        return self.pluginFile

    def initPlugins(self, filename):
        # 首次加载插件运行方法
        pluginName = os.path.splitext(filename)[0]
        plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
        plugin.plugins.activate(self)

    def configPlugins(self, filename):
        # 读取插件配置
        try:
            pluginName = os.path.splitext(filename)[0]
            plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
            self.statusPlugins(pluginName, plugin.plugins.config(self))
            return plugin.plugins.config(self)
        except Exception as re:
            pass

    def loopPlugins(self, filename):
        # 循环执行插件主程序
        pluginName = os.path.splitext(filename)[0]
        plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
        plugin.plugins.render(self)

    def statusPlugins(self, pluginName, pluginInfo):
        # 插件状态显示
        try:
            c.log("[Notice]：正在加载插件：" + pluginInfo["pluginName"],
                  "插件文件：" + pluginName + " 插件版本：" + pluginInfo["Version"],
                  style="#a4ff8f")
        except Exception as re:
            pass


if __name__ == '__main__':
    obj = plugin()
    fileList = obj.loadPlugins()  # 开始加载插件
    try:
        for lists in fileList:  # 第一次调用并初始化插件
            obj.initPlugins(lists)
    except Exception as re:
        pass

    while True:
        time.sleep(2)
        for lists in fileList:
            obj.loopPlugins(lists)
