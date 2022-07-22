"""
异步测试版本
"""
import json
import os
import sys
import time
import atexit
from concurrent.futures import ThreadPoolExecutor

import requests

import pluginMirai

from rich.console import Console

c = Console()  # 实例化控制台输出
t = time.time()  # 程序时间

configList: dict = {}  # 存储每个文件BotID值的数组
globalConfigList: dict = {"Bot": {}}  # 存储全局变量的数组

"""
提示：
sessionConfigList字典里每个键是BotID 每个值是 Session 一个BotID对应一个Session，在this函数里根据每个文件BotID对应的值不同而调用
不同Session值
每个相同的ID使用判断自动跳过，避免重复绑定
"""


class argv:
    # 启动配置处理类
    def __init__(self):
        self.arg: list = sys.argv[1:]  # 获取输入参数
        pass

    def len(self) -> int:
        return len(self.arg)

    def dispose(self):
        if self.len() == 0:
            globalConfigList["startConfig"] = {
                "mod": "normal",
                "log": False,
                "logFile": False
            }
            c.log("[Notice]：当前运行模式为" + globalConfigList["startConfig"]["mod"], style="#a4ff8f")
        else:
            for lists in self.arg:
                if lists == "-debug":
                    globalConfigList["startConfig"] = {
                        "mod": "debug",
                        "log": True,
                        "logFile": False
                    }

                else:
                    globalConfigList["startConfig"] = {
                        "mod": "normal",
                        "log": False,
                        "logFile": False
                    }


class this:

    def __init__(self):
        self.pluginFile = []  # 存储插件文件名称
        self.session = ""  # 存储已经绑定的Session

    # 插件内调用函数类
    def begin(self) -> str:
        pass

    def getSession(self):
        return globalConfigList

    def sendFriend(self, send, msg, tar):
        # 发送好友消息
        """
        发送好友普通消息
        :param send: 发送者ID
        :param msg: 消息字典
        :param tar: 消息发送的目标
        :return:{'code': 0, 'msg': 'success', 'messageId': XXXX}
        """
        headers = {
            'Connection': 'close'
        }
        if len(msg) >= 0:
            message = json.dumps(msg)
            message = '{"sessionKey":"' + self.session + '","target":' + tar + ',"messageChain":[' + message + ']}'
            request = requests.post(url=self.host + ":" + self.port + "/sendFriendMessage", data=str(message),
                                    headers=headers)
            if request.status_code == 200:
                request = json.loads(request.text)
                if request['code'] == 0:
                    self.Debug(request, 5)
                    self.Debug("好友消息发送成功！", 0)
                    return request
                else:
                    self.Debug("发送好友信息失败！", 1)
                    self.Debug(request['msg'], 1)

            else:
                self.Debug("连接请求失败！请检查网络配置！", 2)


class plugin(this):

    # 插件装载触发函数

    def loadPlugins(self):
        # 在plugins中获取插件文件
        try:
            pluginNumber: int = 0
            for pluginName in os.listdir("plugins/"):
                if pluginName.endswith('.py') or not pluginName.startswith("_"):
                    self.configPlugins(pluginName)
                    self.pluginFile.append(str(pluginName))  # 将文件名称添加到数组
                    pluginNumber = pluginNumber + 1
        except Exception as re:

            pass
            print(re)
        c.log("[Notice]：", "已完成 " + str(pluginNumber) + " 个插件装载", style="#a4ff8f")
        return self.pluginFile

    def initPlugins(self, filename):
        # 首次加载插件运行方法
        pluginName = os.path.splitext(filename)[0]
        plugin = __import__("plugins." + pluginName, fromlist=[pluginName], globals=globalConfigList)
        self.statusPlugins(pluginName, self.configPlugins(pluginName))
        plugin.plugins.activate(self, globalConfigList)

    def configPlugins(self, filename):
        # 读取插件配置
        try:
            pluginName = os.path.splitext(filename)[0]
            plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
            return plugin.plugins.config(self)
        except Exception as re:
            pass
            print(re)

    def loopPlugins(self, filename):
        # 循环执行插件主程序
        try:
            pluginName = os.path.splitext(filename)[0]
            plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
            plugin.plugins.render(self)
        except Exception as re:
            pass
            print(re)

    def statusPlugins(self, pluginName, pluginInfo):
        # 插件状态显示
        try:
            c.log("[Notice]：正在加载插件：" + pluginInfo["pluginName"],
                  "插件文件：" + pluginName + ".py 插件版本：" + pluginInfo["Version"],
                  style="#a4ff8f")
        except Exception as re:
            print(re)
            pass

    def shutdownPlugins(self, filename):
        # 关闭插件
        try:
            pluginName = os.path.splitext(filename)[0]
            plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
            plugin.plugins.deactivate(self)
        except Exception as re:
            print(re)
            pass


class emc:
    def __init__(self):
        self.globalSelf = globalConfigList


first = argv()  # 初始化参数读取器
this = this()
obj = plugin()
fileList = obj.loadPlugins()  # 开始加载插件


def listConfigs():
    # 读取配置文件并绑定对应关系
    try:
        for lists in fileList:
            configList[lists] = {
                "BotID": obj.configPlugins(lists)["BotID"]
                , "host": obj.configPlugins(lists)["uri"]
                , "port": obj.configPlugins(lists)["port"]
                , "verifyKey": obj.configPlugins(lists)["verifyKey"]
            }
            # sessionConfigList[obj.configPlugins(lists)["BotID"]] = obj.configPlugins(lists)["verifyKey"]
        # print(configList)
    except Exception as re:
        print(re)
        pass


def instrumentConfig():
    # 用于检测地址和端口是否有效
    version = "未知"
    for lists in configList:
        uri = configList.get(lists)["host"] + ":" + configList.get(lists)["port"] + "/about"
        try:
            request = requests.get(url=uri, timeout=5)
        except Exception as re:
            print(re)
            c.log("[Alert]：文件 " + lists + " 地址或端口有误，详细：查询不到Mirai服务器", style="#fb48a0")
            exit()
        if request.status_code == 200:
            data = json.loads(request.text)
            version = data["data"]["version"]
    c.log("[Notice]：当前Mirai-HTTP-API版本为 " + version + " ，详细: 已查询到Mirai服务器", style="#a4ff8f")


def getSession():
    # 尝试获取session
    # 获取原理：读取文件config方法获取到BotID然后是用对应的BotID查找对应的verifyKey进行绑定请求
    for lists in configList:
        data = {
            "verifyKey": str(configList.get(lists)['verifyKey'])
        }
        uri = str(configList.get(lists)["host"]) + ":" + str(configList.get(lists)["port"]) + "/verify"
        data = json.dumps(data)
        request = requests.post(url=uri, data=data)
        if request.status_code == 200:
            data = json.loads(request.text)
            if data["code"] == 0:
                # 将session写入全局变量字典
                this.session = str(data["session"])
                globalConfigList["Bot"][str(configList.get(lists)['BotID'])] = {
                    "session": data["session"],
                    "host": str(configList.get(lists)["host"]),
                    "port": str(configList.get(lists)["port"])
                }
                c.log("[Notice]：文件 " + lists + " 获取session成功，详细: " + data['session'], style="#a4ff8f")
            else:
                # 发生错误时将全局变量的的session设置为空
                globalConfigList["Bot"][str(configList.get(lists)['BotID'])] = {"session": ""}
                c.log("[Warning]：文件 " + lists + " 中 verifyKey 发生错误，详细：" + data["msg"], style="#f6ff8f")


def bindSession():
    # 尝试绑定session
    for lists in globalConfigList["Bot"]:
        if len(globalConfigList["Bot"].get(lists)["session"]) != 0:
            data = {
                "sessionKey": globalConfigList["Bot"].get(lists)["session"],
                "qq": lists
            }
            uri = str(globalConfigList["Bot"].get(lists)["host"]) + ":" + str(
                globalConfigList["Bot"].get(lists)["port"]) + "/bind"
            data = json.dumps(data)
            request = requests.post(url=uri, data=data)
            if request.status_code == 200:
                data = json.loads(request.text)
                if data["code"] == 0:
                    c.log("[Notice]：BotID " + lists + " 绑定Session成功，详细: " + data['msg'], style="#a4ff8f")
                else:
                    # 发生错误时将全局变量的的session设置为空
                    globalConfigList["Bot"][lists] = {
                        "session": ""
                    }
                    c.log("[Warning]：在绑定BotID " + lists + " 中 BotID 发生错误，详细：" + data["msg"], style="#f6ff8f")


# 框架停止运行时启用
@atexit.register
def quits():
    # 释放资源用
    try:
        # 执行插件内自定义退出函数
        for lists in os.listdir("plugins/"):
            if lists.endswith('.py') or not lists.startswith("_"):
                obj.shutdownPlugins(lists)
                c.log("[Notice]：Shutdown Plugins " + lists + " succeed", style="#a4ff8f")
        # 释放Session
        for lists in globalConfigList["Bot"]:
            if len(globalConfigList["Bot"].get(lists)["session"]) != 0:
                uri = globalConfigList["Bot"].get(lists)["host"] + ":" + globalConfigList["Bot"].get(lists)[
                    "port"] + "/release"
                data = {
                    "sessionKey": globalConfigList["Bot"].get(lists)["session"],
                    "qq": str(lists)
                }
                data = json.dumps(data)
                request = requests.post(url=uri, data=data)
                if request.status_code == 200:
                    data = json.loads(request.text)
                    if data["code"] == 0:
                        c.log("[Notice]：BotID " + lists + " 释放Session成功，详细: " + data["msg"], style="#a4ff8f")
                    else:
                        c.log("[Warning]：在释放BotID " + lists + " 中发生错误，详细：" + data["msg"], style="#f6ff8f")

    except Exception as re:
        pass


def threadPoolOBJ(maxWork: int):
    # 创建新线程池函数
    try:
        pool = ThreadPoolExecutor(maxWork)
        c.log("[Notice]：成功创建容量为" + str(maxWork) + "的线程池", style="#a4ff8f")
        return pool
    except Exception as re:
        pass


# 以插件数量的基础上+3为最大执行数量作为冗余
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
    first.dispose()
    listConfigs()  # 获取配置信息
    instrumentConfig()  # 测试每一个模块提供的地址是否有效
    getSession()  # 获取Session
    print(globalConfigList)
    bindSession()  # 绑定session

    try:
        for lists in fileList:  # 第一次调用并初始化插件
            pool.submit(obj.initPlugins, lists)  # 将初始化函数推到线程池做并发初始化处理
    except Exception as re:
        pass

    loopOBJ()  # 执行循环执行项目
