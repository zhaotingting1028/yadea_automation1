from Core.client import *
from Core.randommer import *
from Core.log import logger



class saveOrUpdate(unittest.TestCase):

    def test_saveOrUpdate_01(self):
        """充电中发生烧车"""
        headers = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsieXN0LWRlbW8iLCJ5c3QteWQtYWZ0ZXJzYWxlcyIsInlzdC15ZC1vbXMiLCJ5c3QteWQtZm9yZWlnbiIsInlzdC15ZC1pbnYiLCJ5c3QteWQtc2FsZSIsInlzdC15ZC1maW5hbmNlIiwiZWxpdGVzbGFuZC1yZXNvdXJjZS1zdnIiLCJ5c3QteWQtbWVzc2FnZSIsInlkLWludi1yZXNvdXJjZS1pZCIsInlkLXB1ci1yZXNvdXJjZS1pZCIsInlzdC15ZHVzZXIiLCJ5c3QteWQtenBtIiwieXN0LXlkLXVzZXIiLCJhZG1pbi1jbGllbnQtdGVzdCIsInlzdC15ZHN5c3RlbSIsInlzdC1zeXN0ZW0iLCJ5c3QteWQtcmVwb3J0IiwieXN0LXlkLXN5c3RlbSIsInlzdC15ZC1leHBvcnQiLCJ5c3QteWQtcHVyIiwidXNlci1yZXNvdXJjZS1pZCIsInlkLXVzZXItcmVzb3VyY2UtaWQiXSwiZXhwIjoxNzE3NzE5Mjg4LCJ1c2VyX25hbWUiOiJxdWFsaXR5X3VzZXIiLCJqdGkiOiJjNzM3MGEyNi01OWUxLTQ3YWQtOWJlZC1hYTNmNTQ5MDA2YzIiLCJjbGllbnRfaWQiOiJxdWFsaXR5Iiwic2NvcGUiOlsiYWxsIl19.ltkjZ5NkF6mzm0bADL4KJ8USCgSsIhZh1gqxkIvE2P754PCuikA5JBHWhqkPqmlHqt_7vt9o5pDDsmQr0DLjYZQ4eemoOGy2ZIlzP0VYUhOujzx-rSiaBUwsgwgohv5aNPBkE-L1SVZ6Rf3aG7AaA9XPqDTpy3lIlK47jQljXT0f-2j9AZREVKzI-_aN-Ldc2a4pica5Dp66PlWAJB1uF4sQqcVZ3fgJr-Oetoi1BC_uMf1YCTvdoolRtPUMcgBubZAW1lVUXifuC6b79MQT50qoXU5PObaotFiZ4AUOsfY8PW5qAad0US4jZ0c4wiDZJF07km7KVkouB1yWxt230g"
        vim = getRandomvim()
        time = gettime()
        client= http_client()
        client.url = "https://dmsuat.yadea.com.cn/yd-quality/critical/saveOrUpdate"
        client.method = method.POST
        client.body_type = body_type.JSON
        client.headers = {"Authorization": headers}
        client.body ={"purchaseDate":"2023-06-02","creatorType":"1","createUserId":"36521","creator":"梁有威","storeName":"锡山雅迪011","storeCode":"A0510001E011","merchantCode":"A0510001","merchantName":"A0510001锡沪西路雅迪","merchantPhone":"18899998888","feedbackPhone":"18899998888","feedbackMan":"锡沪西路雅迪-总管","feedbackDay":time,"vinNo":vim,"happenDate":time,"accidentAttribute":"0","specificAttribute":"","happenPalace":"河北省石家庄市裕华区翟营南大街64号靠近","happenStatus":"0","eventDescription":"我是一个描述","userName":"这是个用户姓名","userPhone":"15100000002","claimStatementList":"1、001材料费\n2、002损失人工费\n3、003场地费","vehicleAttachmentList":[{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/1710826049316cb126585.jpg","name":"OIP-C.jpg","position":0},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/17108260524443217bfab.jpg","name":"R-C - 副本.png","position":1},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/1710826055260fee10f28.jpg","name":"R-C (1).jpg","position":2},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/17108260593098a5dccf1.jpg","name":"R-C.jpg","position":3},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/1710826061877fd369a0c.jpg","name":"R-C.png","position":4}],"articleAttachmentList":[{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/02.6%E9%9B%85%E8%BF%AA%E4%B8%AA%E4%BA%BA%E4%B8%AD%E5%BF%83%20-%20%E6%94%B6%E8%97%8F.png.png","name":"02.6雅迪个人中心 - 收藏.png"},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/02.1%E9%9B%85%E8%BF%AA%E9%A6%96%E9%A1%B5.png.png","name":"02.1雅迪首页.png"},{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/02.2%E9%9B%85%E8%BF%AA%E9%A6%96%E9%A1%B5%E5%AD%90%E5%88%86%E9%A1%B5.png.png","name":"02.2雅迪首页子分页.png"}],"personAttachmentList":[{"attachment":"https://osstest.yadea.com.cn/dms/aftersale/quailty/20240319/1710826321653.jpg.jpg","name":"1710826321653.jpg"}],"produceLocation":"无锡工厂","vinType":"冠能ED30-D-豪华版前碟AC-W—虹彩陨铁灰(Q+HK)","produceDate":"2023-02-21","useDays":291,"hasPersonInjured":"0","hasFireInvolved":"0","isOriginalCharger":"0","isOriginalBattery":"0","hasUseCable":"0"}
        client.send()
        # logger.info("接口请求结果" + ":" + client.res_text)
        msg = client.res_json_parser_log("$.msg")
        logger.info("接口请求结果" + ":" + msg)
        client.check_res_text_contains(msg,"操作成功")
        client.check_status_code()


saveOrUpdate().test_saveOrUpdate_01()