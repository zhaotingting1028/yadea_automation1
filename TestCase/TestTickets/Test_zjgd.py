from Core.client import *
from Core.randommer import *
from Core.log import logger
from TestCase.TestTickets import case_data

class test_zjgd(unittest.TestCase):
    """APP自建救援工单_保内一年内车架号_维修保养电池检测补胎洗车_换件"""
    url = case_data.url
    cookies_token = case_data.cookies_token
    access_token = case_data.access_token
    token = case_data.token
    Phone = getRandomPhone()
    barCode = genNumByLength(9)
    vinNumber1 = case_data.vinNumber1

    def test_zjgd(self):
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



            """查询createOrderV1订单编码"""
            client2 = http_client()
            client2.url = self.url + '/yd-aftersales/repairorder/createOrderV1'
            client2.method = method.POST
            client2.body_type = body_type.JSON
            client2.headers = {"Authorization": self.cookies_token}
            body = {"orderType": 5, "orderSource": 2, "repairManPhone": Orderlist['mobile'], "unitName": Orderlist['empBuName'],
                    "serviceCode":  Orderlist['storeCode'], "repairManCode": Orderlist['empCode'], "unitCode": Orderlist['buCode'], "orderStatus": 3,
                    "repairManName": Orderlist['empName'], "storeName": Orderlist['buName']}
            client2.body =body
            client2.send()
            orderCode = client2.res_json_parser_log("$.data.orderCode")
            msg = client2.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")



            """查询createOrderV1订单编码"""
            client2 = http_client()
            client2.url = self.url + '/yd-aftersales/repairorder/createOrderV1'
            client2.method = method.POST
            client2.body_type = body_type.JSON
            client2.headers = {"Authorization": self.cookies_token}
            body = {"orderType": 5, "orderSource": 2, "repairManPhone": Orderlist['mobile'], "unitName": Orderlist['empBuName'],
                    "serviceCode":  Orderlist['storeCode'], "repairManCode": Orderlist['empCode'], "unitCode": Orderlist['buCode'], "orderStatus": 3,
                    "repairManName": Orderlist['empName'], "storeName": Orderlist['buName']}
            client2.body =body
            client2.send()
            orderCode = client2.res_json_parser_log("$.data.orderCode")
            msg = client2.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")


            """手动新建工单"""
            client3 = http_client()
            client3.url = self.url + '/yd-aftersales/repairorder/updateOrderById'
            client3.method = method.POST
            client3.body_type = body_type.JSON
            client3.headers = {"Authorization": self.cookies_token}
            body = {"repairManPhone": Orderlist['mobile'],"customerPhone": self.Phone,"customerName": "自动化测试","orderCode": orderCode}
            client3.body =body
            client3.send()
            msg = client3.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")


            """根据订单code获取订单编码"""
            client4 = http_client()
            client4.url = self.url + '/yd-aftersales/repairorder/findByOrderCode/' + orderCode
            client4.method = method.GET
            client4.cookies = {"Authorization": self.cookies_token}
            client4.send()
            id = client4.res_json_parser_log("$.data.id")
            msg = client4.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

            """findByBarCode校验绑定码是否可用"""
            client5 = http_client()
            client5.url = self.url + '/yd-aftersales/repairorderentry/findByBarCode?' +'barCode='+ self.barCode
            client5.method = method.GET
            client5.cookies = {"Authorization": self.cookies_token}
            client5.send()
            msg = client5.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

            """维修员获取处理中工单列表"""
            client6 = http_client()
            client6.url = self.url + '/yd-aftersales/queueorder/pendingRepair/' + Orderlist['storeCode']+ '/' + Orderlist['empCode']
            client6.method = method.GET
            client6.cookies = {"Authorization": self.cookies_token}
            client6.send()
            Repair = ("$.data[0].repairUserId","$.data[0].serviceCode","$.data[0].customerPhone","$.data[0].orderCode",
                      "$.data[0].id")
            pendingRepair = {}
            for i in range(0,len(Repair)):
                pending = []
                for j in Repair:
                    pending.append(client6.res_json_parser_log(j))
                pendingRepair['repairUserId_id1'] = pending[0]
                pendingRepair['serviceCode_Code1'] = pending[1]
                pendingRepair['customerPhone_Phone1'] = pending[2]
                pendingRepair['orderCode1'] = pending[3]
                pendingRepair['id_id1'] = pending[3]
            msg = client6.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

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



            """查询getPartIdByBarCode通过一物一码查询配件ID"""
            client8 = http_client()
            client8.url = self.url + '/yd-aftersales/appraise/getPartIdByBarCode'
            client8.method = method.GET
            client8.cookies = {"Authorization": self.cookies_token}
            client8.params = {"barCode": self.barCode}
            client8.send()
            msg = client8.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

            """获取所有故障带明细"""
            client9 = http_client()
            client9.url = self.url + '/yd-aftersales/repairinfo/findAllByInfoId'
            client9.method = method.GET
            client9.cookies = {"Authorization": self.cookies_token}
            client9.send()
            msg = client9.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

            """校验三包期_通过车架号和配件ID查询 CodeAndPartId"""
            client10 = http_client()
            client10.url = self.url + '/yd-aftersales/appraise/getPartIdByBarCode'
            client10.method = method.GET
            client10.cookies = {"Authorization": self.cookies_token}
            client10.params = {"vinNumber": self.vinNumber1,"barCode": self.barCode,"partId": 110081,"orderId": id}
            client10.send()
            msg = client10.res_json_parser_log("$.msg")
            self.assertEqual(msg,"操作成功")

            """完成工单"""
            client13 = http_client()
            client13.url = self.url + '/yd-aftersales/repairorder/updateOrder'
            client13.method = method.POST
            client13.body_type = body_type.JSON
            client13.headers = {"Authorization": self.cookies_token}
            body = {
                "orderType": "3","repairManCode":  Orderlist['empCode'],"repairPhoto": "",
                "repairTypes": [
                    {
                        "symptom": "保养","symptomCause": "电池安装","symptomCauseId": "1448929523720454189","symptomId": "1448928280550838274"
                    },
                    {
                        "symptom": "保养","symptomCause": "电池电压","symptomCauseId": "1448929523720454192","symptomId": "1448928280550838274"
                    },
                    {
                        "symptom": "保养","symptomCause": "电池外观","symptomCauseId": "1448929523720454193","symptomId": "1448928280550838274"
                    }],
                "partsMoney": "30.00",
                "unitCode": Orderlist['buCode'],
                "repairOrderEntrys": [
                    {
                        "barCode": self.barCode,"batteryCode": "","batteryType": "石墨烯电池-南都",
                        "extraHint": "","historyOverflow": "false","isGuarantee": "true","isReplaced": "true",
                        "isReverse": "true","isShowExtra": "false","isTriple": "false",
                        "money": "30.00","needBCode": 0,"needBDate": 0,"needBNum": 0,"number": "1",
                        "partId": 110081,"partsCode": 110081,"partsName": "石墨烯电池-南都",
                        "photo": "","reasonDesc": "漏液","remark": "","showAdd": "true","showDelete": "false"
                    }],
                "repairManName": Orderlist['empName'],"id": id,"brand": "雅迪","operatName": Orderlist['empName'],
                "operatCode": Orderlist['empCode'],"mtcStartTime": gettime_hh(),"unitName": Orderlist['empBuName'],
                "workingHoursMoney": "0.0","totalMoney": "30.00","customerName": "自动化测试","storeLongitude": Orderlist['longitude'],
                "isWash": 1,"serviceCode": Orderlist['storeCode'],"isYadeaCar": "true","orderStatus": 5,
                "isOnline": "false","remark": "",
                "keepInfo": {
                    "nextKeepDate": "2023-12-31 00:00:00","keepCycle": 6,
                    "partInfo": [
                        {
                            "partId": 110081,"partName": "石墨烯电池-南都"
                        }]
                },
                "manualPurchaseTime": "false","settlementLongitude": Orderlist['longitude'],
                "allCutPrice": "0.00","customerPhone": self.Phone,
                "repairManPhone": Orderlist['mobile'],"storeLatitude": Orderlist['latitude'],"vinNumber": self.vinNumber1,
                "manufactureDate": getProduct['saleDate1'],"storeName": Orderlist['buName'],"serviceId": Orderlist['buId'],"productType": 1,
                "relatedProductMoney": "0.0","repairUserId": pendingRepair['repairUserId_id1'],"motorcycleType": getProduct['productName1'],
                "repairType": "维修、保养、电池检测、补胎、洗车","discountMoney": "0.0",
                "batterys": [
                ],
                "batteryStatus": 0,"purchaseTime": getProduct['mfgDate1'],"settlementLatitude": Orderlist['latitude'],"isTrail": 0
            }
            client13.body = body
            client13.send()
            msg = client13.res_json_parser_log("$.msg")
            self.assertEqual(msg, "操作成功")
