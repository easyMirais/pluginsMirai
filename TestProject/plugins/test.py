class plugins:
    def config(self) -> dict:
        # 插件配置项
        config = {
            "pluginName": "测试插件",  # 插件的名字
            "Version": "v1.0.0",  # 插件的版本
            "BotID": "12345678"  # QQBot的号码
        }
        return config

    def activate(self):
        # 在加载插件的过程中加载一次此方法
        print("这是第一次调用此方法！")

    def render(self):
        # 循环运行的主程序方法
        print("正在运行主程序方法")
