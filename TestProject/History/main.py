import os
import time
import atexit

import easyMirai
import api

from rich.console import Console

c = Console()  # 实例化控制台输出



class plugin:

    # 插件装载触发函数

    def __init__(self):
        self.pluginFile = []  # 存储插件文件名称
        self.session = []  # 存储已经绑定的Session

    def loadPlugins(self):
        # 在plugins中获取插件文件
        try:
            for pluginName in os.listdir("../plugins/"):
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
        self.statusPlugins(pluginName, self.configPlugins(pluginName))
        plugin.plugins.activate(self, this)

    def configPlugins(self, filename):
        # 读取插件配置
        try:
            pluginName = os.path.splitext(filename)[0]
            plugin = __import__("plugins." + pluginName, fromlist=[pluginName])

            return plugin.plugins.config(self)
        except Exception as re:
            pass

    def loopPlugins(self, filename):
        # 循环执行插件主程序
        try:
            pluginName = os.path.splitext(filename)[0]
            plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
            plugin.plugins.render(self, this)
        except Exception as re:
            pass

    def statusPlugins(self, pluginName, pluginInfo):
        # 插件状态显示
        try:
            c.log("[Notice]：正在加载插件：" + pluginInfo["pluginName"],
                  "插件文件：" + pluginName + " 插件版本：" + pluginInfo["Version"],
                  style="#a4ff8f")
        except Exception as re:
            pass

    def shutdownPlugins(self, filename):
        # 关闭插件
        try:
            pluginName = os.path.splitext(filename)[0]
            plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
            plugin.plugins.deactivate(self, this)
        except Exception as re:
            pass


class begin(plugin):
    # 初始化mirai类
    pass


class this(easyMirai.Mirai):
    # 插件内调用函数类
    def begin(self) -> str:
        pass


obj = plugin()
fileList = obj.loadPlugins()  # 开始加载插件




# 框架停止运行时启用
@atexit.register
def quits():
    # 释放资源用
    try:
        for lists in os.listdir("../plugins/"):
            if lists.endswith('.py') or not lists.startswith("_"):
                obj.shutdownPlugins(lists)
                c.log("[Notice]：Shutdown Plugins " + lists + " succeed", style="#a4ff8f")
    except Exception as re:
        pass


def loopObject():
    # 运行主程序用
    try:
        time.sleep(1)
        for lists in fileList:
            obj.loopPlugins(lists)
    except Exception as re:
        pass


if __name__ == '__main__':

    listConfigs()

    try:
        for lists in fileList:  # 第一次调用并初始化插件
            obj.initPlugins(lists)
    except Exception as re:
        pass

    while True:
        loopObject()
