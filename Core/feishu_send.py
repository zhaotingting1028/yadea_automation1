import requests
import json
class FeishuTalk():

    # 机器人webhook
    chatGPT_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/1f7fd0ae-b143-4542-aa1c-9d7c7173b835'

    # 发送文本消息
    def sendTextmessage(self, content):
        url = self.chatGPT_url
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        payload_message = {
            "msg_type": "text",
            "content": {
            	# @ 单个用户 &lt;at user_id="ou_xxx"&gt;名字&lt;/at&gt;
                "text": content + "  接口自动化测试报告已生成注意查看"
                # @ 所有人 &lt;at user_id="all"&gt;所有人&lt;/at&gt;
                # "text": content + "&lt;at user_id=\"all\"&gt;test&lt;/at&gt;"
            }
        }
        response = requests.post(url=url, data=json.dumps(payload_message), headers=headers)
        return response.json
