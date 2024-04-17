from Core.client import *
from Core.log import logger


class saveOrUpdate(unittest.TestCase):

    def test_saveOrUpdate_02(self):
        """重复提交"""
        headers = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsieXN0LWRlbW8iLCJ5c3QteWQtYWZ0ZXJzYWxlcyIsInlzdC15ZC1vbXMiLCJ5c3QteWQtZm9yZWlnbiIsInlzdC15ZC1pbnYiLCJ5c3QteWQtc2FsZSIsInlzdC15ZC1maW5hbmNlIiwiZWxpdGVzbGFuZC1yZXNvdXJjZS1zdnIiLCJ5c3QteWQtbWVzc2FnZSIsInlkLWludi1yZXNvdXJjZS1pZCIsInlkLXB1ci1yZXNvdXJjZS1pZCIsInlzdC15ZHVzZXIiLCJ5c3QteWQtenBtIiwieXN0LXlkLXVzZXIiLCJhZG1pbi1jbGllbnQtdGVzdCIsInlzdC15ZHN5c3RlbSIsInlzdC1zeXN0ZW0iLCJ5c3QteWQtcmVwb3J0IiwieXN0LXlkLXN5c3RlbSIsInlzdC15ZC1leHBvcnQiLCJ5c3QteWQtcHVyIiwidXNlci1yZXNvdXJjZS1pZCIsInlkLXVzZXItcmVzb3VyY2UtaWQiXSwiZXhwIjoxNzE3NzE5Mjg4LCJ1c2VyX25hbWUiOiJxdWFsaXR5X3VzZXIiLCJqdGkiOiJjNzM3MGEyNi01OWUxLTQ3YWQtOWJlZC1hYTNmNTQ5MDA2YzIiLCJjbGllbnRfaWQiOiJxdWFsaXR5Iiwic2NvcGUiOlsiYWxsIl19.ltkjZ5NkF6mzm0bADL4KJ8USCgSsIhZh1gqxkIvE2P754PCuikA5JBHWhqkPqmlHqt_7vt9o5pDDsmQr0DLjYZQ4eemoOGy2ZIlzP0VYUhOujzx-rSiaBUwsgwgohv5aNPBkE-L1SVZ6Rf3aG7AaA9XPqDTpy3lIlK47jQljXT0f-2j9AZREVKzI-_aN-Ldc2a4pica5Dp66PlWAJB1uF4sQqcVZ3fgJr-Oetoi1BC_uMf1YCTvdoolRtPUMcgBubZAW1lVUXifuC6b79MQT50qoXU5PObaotFiZ4AUOsfY8PW5qAad0US4jZ0c4wiDZJF07km7KVkouB1yWxt230g"
        client= http_client()
        client.url = "https://dmsuat.yadea.com.cn/yd-quality/critical/saveOrUpdate"
        client.method = method.POST
        client.body_type = body_type.JSON
        client.headers = {"Authorization": headers}
        client.body ={"purchaseDate":"2023-06-02","creatorType":"1","createUserId":"36521","creator":"梁有威","storeName":"锡山雅迪011","storeCode":"A0510001E011","merchantCode":"A0510001","merchantName":"A0510001锡沪西路雅迪","merchantPhone":"18899998888","feedbackPhone":"18899998888","feedbackMan":"主管","feedbackDay":"2024-03-15","vinNo":"779422310106015","happenDate":"2024-03-16","accidentAttribute":"1","specificAttribute":"这是个具体属性","happenPalace":"这是一个地点","happenStatus":"1","eventDescription":"我是一个描述","userName":"这是个用户姓名","userPhone":"15100000002","claimStatementList":"1、001材料费\n2、002损失人工费\n3、003场地费","vehicleAttachmentList":[{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/1710831644509ec23aabf.jpg","name":"test.jpg","position":0},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/17108317290131190fe26.jpg","name":"test.jpg","position":1},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/17108317382751fbcec80.jpg","name":"test.jpg","position":2},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/1710831759824d4599eb2.jpg","name":"test.jpg","position":3}],"articleAttachmentList":[],"personAttachmentList":[{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/test.jpg.jpg","name":"test.jpg"}],"produceLocation":"无锡工厂","vinType":"冠能ED30-D-豪华版前碟AC-W—虹彩陨铁灰(Q+HK)","produceDate":"2023-02-21","useDays":291,"hasFireInvolved":"0","hasPersonInjured":"0"}
        client.send()
        logger.info("接口请求结果" + ":" + client.res_text)
        msg = client.res_json_parser_log("$.msg")
        client.check_res_text_contains(msg, "提交失败，该质量反馈已存在")
        client.check_status_code()
