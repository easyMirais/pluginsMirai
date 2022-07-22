import json

import requests
from main import plugin as obj


class miraiConnect(obj):
    # 用于创建Mirai基本联系信息
    def __init__(self, obc):
        super().__init__()
        self.key = obc
        self.port = host
        self.host = port

    def getSession(self):
        # 获取session状态码
        """
        获取session码
        :return:{'code': 0, 'session': 'XXXX'}
        """
        headers = {
            'Connection': 'close'
        }
        request = requests.post(url=self.host + ":" + self.port + "/verify", data='{"verifyKey": "' + self.key + '"}',
                                headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.session = request['session']
                return request

    def bindSession(self) -> str:
        # 绑定session到QQ机器人
        """
        绑定Session到QQ机器人
        :return: XXXX
        """
        headers = {
            'Connection': 'close'
        }
        request = requests.post(url=self.host + ":" + self.port + "/bind",
                                data='{"sessionKey": "' + self.session + '","qq": ' + self.qid + '}', headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                return self.session

    def releaseSession(self):
        # 释放session到QQBot
        """
        释放已经绑定Bot的Session
        :return: {'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        request = requests.post(url=self.host + ":" + self.port + "/release",
                                data='{"sessionKey": "' + self.session + '","qq": ' + self.qid + '}', headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                return request
