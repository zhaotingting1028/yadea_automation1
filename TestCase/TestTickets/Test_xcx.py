from Core.client import *
from Core.randommer import *
from Core.log import logger
from TestCase.TestTickets import case_data

class test_xcx(unittest.TestCase):

    """小程序发起道路救援"""
    url = case_data.url
    cookies_token = case_data.cookies_token
    access_token = case_data.access_token
    token = case_data.token
    def test_xcx(self):
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

            """获取门店信息"""
            client2 = http_client()
            client2.url = self.url + '/yd-user/org/orgStore/getStoreByBuId/' + Orderlist['serviceId'] + '?'
            client2.method = method.GET
            client2.cookies = {"Authorization": self.token}
            client2.send()
            msg = client2.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")
            getStoreByBuId = ("$.data.appAddrVo.latitude","$.data.appAddrVo.longitude","$.data.appAddrVo.city",
                      "$.data.appAddrVo.province","$.data.appAddrVo.detailAddr","$.data.serviceCode")
            ByBuId = {}
            for i in range(0, len(getStoreByBuId)):
                getStore = []
                for j in getStoreByBuId:
                    getStore.append(client2.res_json_parser_log(j))
                ByBuId['latitude1'] = getStore[0]
                ByBuId['longitude1'] = getStore[1]
                ByBuId['city'] = getStore[2]
                ByBuId['province'] = getStore[3]
                ByBuId['detailAddr'] = getStore[4]
                ByBuId['serviceCode'] = getStore[5]

            """附近门店接口by省市区"""
            client3 = http_client()
            client3.url = self.url + '/yd-aftersales/applets/order/nearbyStores'
            client3.method = method.POST
            client3.body_type = body_type.JSON
            client3.headers = {"Authorization": self.cookies_token}
            client3.body = {"latitude": str(ByBuId['latitude1']),"longitude": str(ByBuId['longitude1'])}
            client3.send()
            msg = client3.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")


            """发起道路救援前检查数据"""
            client4 = http_client()
            client4.url = self.url + '/yd-aftersales/applets/order/checkRoadRescue'
            client4.method = method.POST
            client4.body_type = body_type.JSON
            client4.headers = {"Authorization": self.cookies_token}
            client4.body ={"latitude":str(ByBuId['latitude1']),"longitude":str(ByBuId['longitude1'])}
            client4.send()
            msg = client4.res_json_parser_log("$.data")
            self.assertEqual(msg,"可接单")

            """发起救援工单"""
            client5 = http_client()
            client5.url = self.url + '/yd-aftersales/applets/order/beginRoadRescue'
            client5.method = method.POST
            client5.body_type = body_type.JSON
            client5.headers = {"Authorization": self.token}
            Phone = getRandomPhone()
            body = {"customerPhone": Phone, "repairUserId": Phone, "customerName": "", "orderSource": 1,
             "orderType": 1, "province": ByBuId['province'], "city": ByBuId['city'], "region": "测试区", "address": ByBuId['detailAddr'],
             "longitude": ByBuId['longitude1'], "latitude": ByBuId['latitude1']}
            client5.body =body
            client5.send()
            msg = client5.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

