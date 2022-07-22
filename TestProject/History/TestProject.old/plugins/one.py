"""
pluginMirai插件模版
"""

import core

class plugins:
    def config(self) -> dict:
        # 插件配置项
        config = {
            "pluginName": "想管理者发送信息插件",  # 插件的名字
            "Version": "v1.0.0",  # 插件的版本
            "uri": "http://127.0.0.1",  # MiraiHTTPAPI接口地址
            "port": "8080",  # MiraiHTTPAPI端口地址
            "verifyKey": "INITKEYxWntQVgk",  # 接口连接密钥
            "BotID": "2508417507"  # QQBot的号码
        }
        return config

    def activate(self, session):
        # 在加载插件的过程中加载一次此方法
        print(session)

    def render(self):
        # 循环运行的主程序方法
        pass

    def deactivate(self):
        # 框架关闭时运行 用于释放一些资源使用
        pass
