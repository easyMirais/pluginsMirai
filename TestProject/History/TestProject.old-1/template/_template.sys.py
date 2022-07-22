"""
pluginMirai系统级插件模版
"""


class plugins:

    def deactivate(self):
        # 框架关闭时运行 用于释放一些资源使用
        print("正在运行退出程序操作方法")
