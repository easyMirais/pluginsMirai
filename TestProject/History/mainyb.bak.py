"""
异步测试版本
"""

import os
import time
import atexit
from concurrent.futures import ThreadPoolExecutor

import requests

import easyMirai

from rich.console import Console

c = Console()  # 实例化控制台输出
t = time.time()  # 程序时间

botIDConfigList: dict = {}  # 存储每个文件BotID值的数组
verifyKeyConfigList: dict = {}  # 存储每个文件verifyKey值的数组
sessionConfigList: dict = {}  # 存储每个文件BotID所绑定的session值
hostConfigList: dict = {}  # 存储每个文件BotID所绑定的host值
portConfigList: dict = {}  # 存储每个文件BotID所绑定的port值

"""
提示：
sessionConfigList字典里每个键是BotID 每个值是 Session 一个BotID对应一个Session，在this函数里根据每个文件BotID对应的值不同而调用
不同Session值
每个相同的ID使用判断自动跳过，避免重复绑定
"""


class st:
    pass


class plugin(st):

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


class this(easyMirai.Mirai):
    def begin(self) -> str:
        pass


obj = plugin()
fileList = obj.loadPlugins()  # 开始加载插件


def listConfigs():
    # 读取配置文件并绑定对应关系
    try:
        for lists in fileList:
            botIDConfigList[lists] = obj.configPlugins(lists)["BotID"]
            verifyKeyConfigList[obj.configPlugins(lists)["BotID"]] = obj.configPlugins(lists)["verifyKey"]
            hostConfigList[obj.configPlugins(lists)["BotID"]] = obj.configPlugins(lists)["uri"]
            portConfigList[obj.configPlugins(lists)["BotID"]] = obj.configPlugins(lists)["port"]
            # sessionConfigList[obj.configPlugins(lists)["BotID"]] = obj.configPlugins(lists)["verifyKey"]
    except Exception as re:
        pass
    print(botIDConfigList, verifyKeyConfigList)


def getSession():
    # 尝试获取session
    # 获取原理：读取文件config方法获取到BotID然后是用对应的BotID查找对应的verifyKey进行绑定请求
    for lists in verifyKeyConfigList:
        print(lists, verifyKeyConfigList.get(lists))
        requset = requests.post("")


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


def threadPoolOBJ(maxWork: int):
    # 创建新线程池函数
    pool = ThreadPoolExecutor(maxWork)
    c.log("[Notice]：成功创建容量为" + str(maxWork) + "的线程池", style="#a4ff8f")
    return pool


# 以插件数量的基础上+3为最大执行数量
pool = threadPoolOBJ(len(fileList) + 3)


def loopOBJ():
    # 运行主程序用
    while True:
        try:
            time.sleep(1)
            for lists in fileList:
                pool.submit(obj.loopPlugins, lists)
        except Exception as re:
            pass


if __name__ == '__main__':
    listConfigs()
    try:
        for lists in fileList:  # 第一次调用并初始化插件
            pool.submit(obj.initPlugins, lists)  # 将初始化函数推到线程池做并发初始化处理
    except Exception as re:
        pass
    getSession()
    loopOBJ()
