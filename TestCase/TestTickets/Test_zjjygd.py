
from Core.log import logger
from Core.client import *
from Core.randommer import *
from TestCase.TestTickets import case_data



class test_zjjy(unittest.TestCase):
    """01,APP自建救援工单_保外过三包期_维修单_换件"""
    url = case_data.url
    token=case_data.cookies_token
    access_token = case_data.access_token
    onecode1 = case_data.onecode1
    vim = case_data.vim

    def test_zjjy(self):
        """查询users_id"""
        client= http_client()
        client.url = self.url + '/yst/ydsystem/sys/users/current'
        client.method = method.GET
        client.cookies = {"Authorization": self.token}
        client.params = {"access_token": self.access_token}
        client.send()
        id = client.res_json_parser("$.data.id")
        msg = client.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")


        """查询findEmpByUserId"""
        client1 = http_client()
        client1.url = self.url + '/yd-user/employee1/findEmpByUserId/'+ id[0]+'?'
        client1.method = method.GET
        client1.cookies = {"Authorization": self.token}
        client1.params = {"afterSaleFLag": 1}
        client1.send()
        buName = client1.res_json_parser_log("$.data.buName")
        mobile =client1.res_json_parser_log("$.data.mobile")
        storeCode = client1.res_json_parser_log("$.data.storeDetailVOS[0].storeCode")
        empCode = client1.res_json_parser_log("$.data.empCode")
        buCode = client1.res_json_parser_log("$.data.buCode")
        empName = client1.res_json_parser_log("$.data.empName")
        empBuName = client1.res_json_parser_log("$.data.empBuName")
        buId = client1.res_json_parser_log("$.data.buId")
        longitude = client1.res_json_parser_log("$.data.longitude")
        latitude = client1.res_json_parser_log("$.data.latitude")
        empType = client1.res_json_parser_log("$.data.empType")
        msg = client1.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

        """查询createOrderV1订单编码"""
        client2 = http_client()
        client2.url = self.url+'/yd-aftersales/repairorder/createOrderV1'
        client2.method = method.POST
        client2.body_type = body_type.JSON
        client2.headers = {"Authorization": self.token}
        client2.body = {
            "orderType": 3,
            "orderSource": 2,
            "repairManPhone": mobile,
            "unitName": empBuName,
            "serviceCode": storeCode,
            "repairManCode": empCode,
            "unitCode": buCode,
            "orderStatus": 3,
            "repairManName": empName,
            "storeName": buName
        }
        client2.send()
        orderCode = client2.res_json_parser_log("$.data.orderCode")
        msg = client2.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

        """手动新建工单"""
        phone = getRandomPhone()
        client3 = http_client()
        client3.url = self.url+'/yd-aftersales/repairorder/updateOrderById'
        client3.method = method.POST
        client3.body_type = body_type.JSON
        client3.headers = {"Authorization": self.token}
        client3.body = {"repairManPhone": mobile,"customerPhone": phone,"customerName": "自动化测试","orderCode": orderCode}
        client3.send()
        msg = client3.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

        """根据订单code获取订单编码"""
        findByOrderCodeurl=self.url+'/yd-aftersales/repairorder/findByOrderCode/'+orderCode+'?'
        client4 = http_client()
        client4.url = findByOrderCodeurl
        client4.method = method.GET
        client4.cookies = {"Authorization": self.token}
        client4.params = {"afterSaleFLag": 1}
        client4.send()
        id1= client4.res_json_parser_log("$.data.id")
        msg = client4.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

        """查询getRepairOrderlist救援工单列表"""
        client5 = http_client()
        client5.url = self.url+'/yd-aftersales/repairorder/getRepairOrderlist'
        client5.method = method.POST
        client5.body_type = body_type.JSON
        client5.headers = {"Authorization": self.token}
        client5.body = {
            "status1": 2,
            "serviceCode": storeCode,
            "serviceId": buId,
            "longitude": longitude,
            "dispatchMode": 1,
            "latitude": latitude,
            "repairManCode": empCode,
            "type": empType,
            "orderStatus": 3
        }
        client5.send()
        orderCode1 = client5.res_json_parser_log("$.data[0].orderCode")
        id2=client5.res_json_parser_log("$.data[0].id")
        repairUserId=client5.res_json_parser_log("$.data[0].repairUserId")
        msg = client5.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

        """根据订单code获取订单编码"""
        barCode=genNumByLength(9)
        findByOrderCodeurl = self.url+'/yd-aftersales/repairorderentry/findByBarCode' + '?'+ 'barCode='+ barCode
        client6 = http_client()
        client6.url = findByOrderCodeurl
        client6.method = method.GET
        client6.cookies = {"Authorization": self.token}
        client6.send()
        msg = client6.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

        """根据车架号查询车辆信息"""
        client7 = http_client()
        vinNumber= self.vim
        getvimurl=self.url+'/yst/ydforeign/app/repair/quality/getProduct' +'?'
        client7.url = getvimurl
        client7.method = method.GET
        client7.cookies = {"Authorization": self.token}
        client7.params = {"vinNumber": vinNumber}
        client7.send()
        productName1 = client7.res_json_parser_log("$.data[0].productName")
        saleDate1= client7.res_json_parser_log("$.data[0].saleDate")
        mfgDate1 = client7.res_json_parser_log("$.data[0].mfgDate")
        msg = client7.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

        """查询getPartIdByBarCode通过一物一码查询配件ID"""
        client8 = http_client()
        onecode = self.onecode1[1]
        getPartIdByBarCodeurl = self.url+'/yd-aftersales/appraise/getPartIdByBarCode'+ '?'
        client8.url = getPartIdByBarCodeurl
        client8.method = method.GET
        client8.cookies = {"Authorization": self.token}
        client8.params = {"barCode": onecode}
        client8.send()
        partId1 = client8.res_json_parser_log("$.data.partId")
        partName1 = client8.res_json_parser_log("$.data.partName")
        msg = client8.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

        """校验三包期_通过车架号和配件ID查询 CodeAndPartId"""
        client9 = http_client()
        getPartIdByBarCodeAndPartIdurl =self.url+"/yd-aftersales/appraise/appraiseByVinNumberAndBarCodeAndPartId" + '?'
        client9.url = getPartIdByBarCodeAndPartIdurl
        client9.method = method.GET
        client9.cookies = {"Authorization": self.token}
        client9.params = {"barCode": barCode,
                          "vinNumber": vinNumber,
                          "partId": partId1,
                          "orderId": id1}

        client9.send()
        reason = client9.res_json_parser_log("$.data.reason")
        self.assertEqual(reason, "已超过配件的购车日期三包标准")

        """创建工单"""
        client10 = http_client()
        mtcStartTime=gettime_hh()
        client10.url = self.url+'/yd-aftersales/repairorder/updateOrder'
        client10.method = method.POST
        client10.body_type = body_type.JSON
        client10.headers = {"Authorization": self.token}
        client10.body = {"orderType": 3,"repairManCode": empCode,"repairPhoto": "","repairTypes": [],"partsMoney": "30.00",
                        "unitCode": buCode,"repairOrderEntrys": [{"barCode": barCode,"batteryCode": "","batteryType": "鼓刹","extraHint": "",
		                "historyOverflow": "true","isGuarantee": "false","isReplaced": "true","isReverse": "false","isShowExtra": "false",
		                "isTriple": "false","money": "30.00","needBCode": 0,"needBDate": 0,"needBNum": 0,"number": "1","partId":  partId1 ,
		                "partsCode": partId1 ,"partsName": partName1,"photo": "","reasonDesc": "报警迟钝","remark": "","showAdd": "true","showDelete": "false",
		                "unableReason": reason}], "repairManName": empName,"id": id1,"brand": "雅迪","operatName": empName,"operatCode": empCode,
                        "mtcStartTime": mtcStartTime,"unitName": empBuName,"workingHoursMoney": "0.0","totalMoney": "30.00","customerName": "自动化测试",
                        "storeLongitude": longitude,"isWash": 0,"serviceCode": storeCode,"isYadeaCar": "true","orderStatus": 5,"isOnline": "false",
                        "remark": "","keepInfo": {},"manualPurchaseTime": "false","settlementLongitude": longitude,"allCutPrice": "0.00","customerPhone": phone,
                        "repairManPhone": mobile,"storeLatitude": latitude,"vinNumber": vinNumber,"manufactureDate": saleDate1,"storeName": buName,
                        "serviceId": buId,"productType": 1,"relatedProductMoney": "0.0","repairUserId": repairUserId,"motorcycleType": productName1,
                        "repairType": "维修","discountMoney": "0.0","batterys": [],"batteryStatus": -1,"purchaseTime": mfgDate1,"settlementLatitude": latitude,
                        "isTrail": 0}
        client10.send()
        msg = client10.res_json_parser_log("$.msg")
        self.assertEqual(msg, "操作成功")

