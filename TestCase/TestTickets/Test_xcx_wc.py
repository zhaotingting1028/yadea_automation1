from Core.client import *
from Core.randommer import *
from Core.log import logger
from TestCase.TestTickets import case_data

class test_xcx_wc(unittest.TestCase):

    """小程序发起道路救援_APP接单_修件"""
    url = case_data.url
    cookies_token = case_data.cookies_token
    access_token = case_data.access_token
    token = case_data.token
    # 一年以内车架号
    vinNumber1 = case_data.vinNumber1

    def test_xcx_wc(self):
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


            """获取待接单救援工单列表"""
            client6 = http_client()
            client6.url = self.url + '/yd-aftersales/repairorder/getRepairOrderlist'
            client6.method = method.POST
            client6.body_type = body_type.JSON
            client6.headers = {"Authorization": self.cookies_token}
            body={"serviceCode": ByBuId['serviceCode'],"repairManCode": Orderlist['empCode'],"latitude": Orderlist['latitude'],"orderStatus": 2,
                          "type": "17","dispatchMode": "1","status1": 2,"serviceId": Orderlist['serviceId'],"longitude": Orderlist['longitude']}
            client6.body =body
            client6.send()
            parser = ("$.data[0].repairUserId", "$.data[0].serviceCode","$.data[0].customerPhone", "$.data[0].orderCode","$.data[0].id")
            Orderlist1 = {}
            for i in range(0,len(parser)):
                data_list1 = []
                for j in parser:
                    data_list1.append(client6.res_json_parser_log(j))
                Orderlist1['repairUserId_id'] = data_list1[0]
                Orderlist1['serviceCode_Code'] = data_list1[1]
                Orderlist1['customerPhone_Phone'] = data_list1[2]
                Orderlist1['orderCode'] = data_list1[3]
                Orderlist1['id_id'] = data_list1[4]


            """根据车架号查询车辆信息"""
            client7 = http_client()
            client7.url = self.url + '/yst/ydforeign/app/repair/quality/getProduct' + '?'
            client7.method = method.GET
            client7.cookies = {"Authorization": self.cookies_token}
            client7.params = {"vinNumber": self.vinNumber1}
            client7.send()
            msg = client7.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")
            parser = ("$.data[0].productName","$.data[0].saleDate","$.data[0].mfgDate")
            getProduct = {}
            for i in range(0, len(parser)):
                getProduct1 = []
                for j in parser:
                    getProduct1.append(client7.res_json_parser_log(j))
                getProduct['productName1'] = getProduct1[0]
                getProduct['saleDate1'] = getProduct1[1]
                getProduct['mfgDate1'] = getProduct1[2]


            """维修员接单"""
            client8 = http_client()
            client8.url = self.url + '/yd-aftersales/repairorder/updateOrder'
            client8.method = method.POST
            client8.body_type = body_type.JSON
            client8.headers = {"Authorization": self.cookies_token}
            body={"operatCode": Orderlist['empCode'],"orderLatitude": "","unitName": Orderlist['empBuName'],"repairUserId": Orderlist1['repairUserId_id'],
	              "serviceCode": Orderlist1['serviceCode_Code'],"repairManCode": Orderlist['empCode'],"orderStatus": "3","customerName": "-",
	              "customerPhone": Orderlist1['customerPhone_Phone'],"repairManPhone": Orderlist['mobile'],"unitCode": Orderlist['buCode'],"repairManName": Orderlist['empName'],
	              "orderLongitude": "","storeName": Orderlist['buName'],"orderCode": Orderlist1['orderCode'],"id": Orderlist1['id_id'],"serviceId": Orderlist['serviceId'],
                  "operatName": Orderlist['empName']}
            client8.body =body
            client8.send()
            msg = client8.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

            """维修员获取处理中工单列表"""
            client9 = http_client()
            client9.url = self.url + '/yd-aftersales/repairorder/getRepairOrderlist'
            client9.method = method.POST
            client9.body_type = body_type.JSON
            client9.headers = {"Authorization": self.cookies_token}
            body={"serviceCode": ByBuId['serviceCode'], "repairManCode": Orderlist['empCode'],
             "latitude": Orderlist['latitude'], "orderStatus": 3,"type": "17", "dispatchMode": "1",
             "status1": 2, "serviceId": Orderlist['serviceId'],"longitude": Orderlist['longitude']}
            client9.body =body
            client9.send()
            msg = client9.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")



            """小程序确认到达"""
            client10 = http_client()
            client10.url = self.url + '/yd-aftersales/repairorder/updateOrder'
            client10.method = method.POST
            client10.body_type = body_type.JSON
            client10.headers = {"Authorization": self.cookies_token}
            body1={"operatCode": Orderlist['empCode'],"unitName": Orderlist['empBuName'],"repairUserId": Orderlist1['repairUserId_id'],
	              "serviceCode": Orderlist1['serviceCode_Code'],"repairManCode": Orderlist['empCode'],"orderStatus": "4",
                  "repairLatitude": Orderlist['latitude'],"customerPhone": Orderlist1['customerPhone_Phone'],"repairManPhone": Orderlist['mobile'],
                  "unitCode": Orderlist['buCode'],"repairManName": Orderlist['empName'],"storeName": Orderlist['buName'],
                  "orderCode": Orderlist1['orderCode'],"id": Orderlist1['id_id'],"serviceId": Orderlist['serviceId'],
                  "repairLongitude": Orderlist['longitude'],"operatName": Orderlist['empName']}

            client10.body =body1
            client10.send()
            msg = client10.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")


            """更新经纬度"""
            client11 = http_client()
            client11.url = self.url + '/yd-aftersales/repairorder/updateOrderLngAndLat' + '?'
            client11.method = method.GET
            client11.cookies = {"Authorization": self.cookies_token}
            client11.params = {"orderCode": Orderlist1['orderCode'],"repairLongitude": ByBuId['longitude1'],"repairLatitude": ByBuId['latitude1']}
            client11.send()
            msg = client11.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")


            """获取所有故障件明细"""
            client12 = http_client()
            client12.url = self.url + '/yd-aftersales/repairinfo/findAllByInfoId' + '?'
            client12.method = method.GET
            client12.cookies = {"Authorization": self.cookies_token}
            client12.send()
            msg = client12.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")


            """完成工单"""
            client13 = http_client()
            client13.url = self.url + '/yd-aftersales/repairorder/updateOrder'
            client13.method = method.POST
            client13.body_type = body_type.JSON
            client13.headers = {"Authorization": self.cookies_token}
            body={"orderType": "1","repairManCode": Orderlist['empCode'],"repairPhoto": "","repairTypes": [],"partsMoney": "30.00","unitCode": Orderlist['buCode'],
                "repairOrderEntrys": [{"barCode": "","batteryCode": "","batteryType": "碟刹盘","extraHint": "","historyOverflow": "false","isGuarantee": "true",
                "isReplaced": "false","isReverse": "true","isShowExtra": "false","isTriple": "false","money": "30.00","needBCode": 0,"needBDate": 0,"needBNum": 0,
                "number": "1","partId": 110026,"partsCode": 110026,"partsName": "碟刹盘","photo": "","reasonDesc": "变形","remark": "",
                "showAdd": "true","showDelete": "false"}],"repairManName":  Orderlist['empName'],"id": Orderlist1['id_id'],"brand": "雅迪","operatName": Orderlist['empName'],
                "operatCode": Orderlist['empCode'],"mtcStartTime": gettime_hh(),"unitName": Orderlist['empBuName'],"workingHoursMoney": "0.0","totalMoney": "30.00",
                "customerName": "-","storeLongitude": Orderlist['longitude'],"isWash": 0,"serviceCode": Orderlist1['serviceCode_Code'],"isYadeaCar": "true","orderStatus": 5,
                "isOnline": "false","remark": "","keepInfo": {},"manualPurchaseTime": "false","settlementLongitude": Orderlist['longitude'],"allCutPrice": "0.00",
                "customerPhone": Orderlist1['customerPhone_Phone'],"repairManPhone": Orderlist['mobile'],"storeLatitude": Orderlist['latitude'],"vinNumber": self.vinNumber1,"manufactureDate": getProduct['saleDate1'],
                "storeName": Orderlist['buName'],"serviceId": Orderlist['serviceId'],"productType": 1,"relatedProductMoney": "0.0","repairUserId": Orderlist1['repairUserId_id'],
                "motorcycleType": getProduct['saleDate1'],"repairType": "维修","discountMoney": "0.0","batterys": [],"batteryStatus": -1,"purchaseTime": getProduct['mfgDate1'],
                "settlementLatitude": Orderlist['latitude'],"isTrail": 0}
            client13.body =body
            client13.send()
            msg = client13.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")



