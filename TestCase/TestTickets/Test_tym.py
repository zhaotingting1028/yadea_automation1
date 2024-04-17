from Core.client import *
from Core.randommer import *
from Core.log import logger
from TestCase.TestTickets import case_data


class test_tym(unittest.TestCase):
    """扫太阳码到店维修"""
    url = case_data.url
    cookies_token = case_data.cookies_token
    access_token = case_data.access_token
    token = case_data.token
    userId = case_data.userId
    userPhone = getRandomPhone()

    def test_tym(self):
            """查询users_id"""
            client = http_client()
            client.url = self.url + '/yst/ydsystem/sys/users/current'
            client.method = method.GET
            client.cookies = {"Authorization": self.cookies_token}
            client.params = {"access_token": self.access_token}
            client.send()
            msg = client.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")
            id = client.res_json_parser("$.data.id")


            """查询findEmpByUserId"""
            client1 = http_client()
            client1.url = self.url + '/yd-user/employee1/findEmpByUserId/' + id[0] + '?'
            client1.method = method.GET
            client1.cookies = {"Authorization": self.token}
            client1.params = {"afterSaleFLag": 1}
            client1.send()
            msg = client1.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")
            findEmpByUserId = ("$.data.buName","$.data.mobile","$.data.storeDetailVOS[0].storeCode","$.data.empCode",
                      "$.data.buCode","$.data.empName","$.data.empBuName","$.data.buId","$.data.longitude",
                      "$.data.latitude","$.data.empType","$.data.storeDetailVOS[0].id")
            Orderlist = {}
            for i in range(0,len(findEmpByUserId)):
                findEmp = []
                for j in findEmpByUserId:
                    findEmp.append(client1.res_json_parser_log(j))
                Orderlist['buName'] = findEmp[0]
                Orderlist['mobile'] = findEmp[1]
                Orderlist['storeCode'] = findEmp[2]
                Orderlist['empCode'] = findEmp[3]
                Orderlist['buCode'] = findEmp[4]
                Orderlist['empName'] = findEmp[5]
                Orderlist['empBuName'] = findEmp[6]
                Orderlist['buId'] = findEmp[7]
                Orderlist['longitude'] = findEmp[8]
                Orderlist['latitude'] = findEmp[9]
                Orderlist['empType'] = findEmp[10]
                Orderlist['serviceId'] = findEmp[11]



            """通过店铺id获取店铺详细信息"""
            client2 = http_client()
            client2.url = self.url + '/yd-aftersales/applets/queue/getOrgStoreDetail/' + Orderlist['buId'] + '?'
            client2.method = method.GET
            client2.cookies = {"Authorization": self.cookies_token}
            client2.send()
            msg = client2.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")
            getOrgStoreDetail = ("$.data.storeName","$.data.id")
            StoreDetail = {}
            for i in range(0, len(getOrgStoreDetail)):
                getOrg = []
                for j in getOrgStoreDetail:
                    getOrg.append(client2.res_json_parser_log(j))
                StoreDetail['storeName'] = getOrg[0]
                StoreDetail['serviceId_id'] = getOrg[1]


            """小程序取号"""
            client3 = http_client()
            client3.url = self.url + '/yd-aftersales/applets/queue/queueNum'
            client3.method = method.POST
            client3.body_type = body_type.JSON
            client3.headers = {"Authorization": self.cookies_token}
            client3.body = {"isRepair": 1,"isMaintain": 1,"isWash": 1,"serviceCode":  Orderlist['storeCode'],"serviceId": Orderlist['serviceId'],
                            "serviceName": StoreDetail['storeName'],"servicePhone": "","sex": 1,"userId": self.userId,"userName": "123456",
                            "userPhone": self.userPhone,"orderSource": 1,"unitName": Orderlist['empBuName'],"unitCode":  Orderlist['buCode']}
            client3.send()
            msg = client3.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")



            """查询待接单列表"""
            client4 = http_client()
            client4.url = self.url + '/yd-aftersales/queueorder/findRepairByCode/' + Orderlist['serviceId'] + '/' + Orderlist['empCode']
            client4.method = method.GET
            client4.headers = {"Authorization": self.cookies_token}
            client4.send()
            msg = client4.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")
            id_id = client4.res_json_parser_log('$.data.id')

            """开始维修"""
            client5 = http_client()
            client5.url = self.url + '/yd-aftersales/queueorder/updateRepair'
            client5.method = method.POST
            client5.body_type = body_type.JSON
            client5.headers = {"Authorization": self.cookies_token}
            client5.body = {"id": id_id,"repairManCode": Orderlist['empCode'],"repairManName": Orderlist['empName'],"repairManPhone": Orderlist['mobile'],
	                        "repairManStation": 1,"repairUserId": self.userId,"serviceCode": Orderlist['storeCode'],
                            "serviceId": StoreDetail['serviceId_id']}
            client5.send()
            msg = client5.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

            """取消维修"""
            client6 = http_client()
            client6.url = self.url + '/yd-aftersales/queueorder/cancelOrder'
            client6.method = method.POST
            client6.body_type = body_type.JSON
            client6.headers = {"Authorization": self.cookies_token}
            client6.body = {"operatCode": Orderlist['empCode'],"id": id_id,"cancelReason": "其他","operatName": Orderlist['empName']}
            client6.send()
            msg = client6.res_json_parser_log("$.data")
            self.assertEqual(msg, "取消成功")
