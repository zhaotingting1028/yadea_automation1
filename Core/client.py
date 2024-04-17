import unittest

import requests
from lxml import etree
import jsonpath
import json
from xml.etree import ElementTree
import random

class method:
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class body_type:
    FORM = "application/x-www-form-urlencoded"
    JSON = "application/json"
    XML = "text/xml"
    FILES = "files"


class http_client():

    def __init__(self):
        self.url = ""
        self.method = ""
        self.params = {}
        self.cookies = {}
        self.headers = {}
        self.body_type = None
        self.body = {}
        self.res = None

    def set_param(self, key, value):
        self.params[key] = value

    def set_cookie(self, key, value):
        self.cookies[key] = value

    def set_header(self, key, value):
        self.headers[key] = value

    def send(self):
        if self.url:
            if self.method == method.GET:
                self.res = requests.get(url=self.url, params=self.params,
                                        cookies=self.cookies, headers=self.headers)
            elif self.method == method.POST:
                if self.body_type:
                    if self.body_type == body_type.FORM:
                        # 如果是form表单
                        self.set_header("Content-Type", "application/x-www-form-urlencoded")
                        self.res = requests.post(url=self.url, params=self.params,
                                                 cookies=self.cookies, headers=self.headers,
                                                 data=self.body)
                    elif self.body_type == body_type.JSON:
                        # 如果是json
                        self.set_header("Content-Type", "application/json")
                        self.res = requests.post(url=self.url, params=self.params,
                                                 cookies=self.cookies, headers=self.headers,
                                                 json=self.body)
                    elif self.body_type == body_type.XML:
                        # 如果是xml  用户传递的参数：{"xml":"xxxxxxxxxxxxxxxxxxxxxxxxxxx"}
                        self.set_header("Content-Type", "text/xml")
                        self.res = requests.post(url=self.url, params=self.params,
                                                 cookies=self.cookies, headers=self.headers,
                                                 data=self.body["xml"])
                    elif self.body_type == body_type.FILES:
                        # 如果是上传文件接口，复合式表单  用户传递参数：
                        # {"png1"："c://1.png", "png2": "c://2.png"}
                        # {"png1": open('c://1.png', 'rb'), "png2": open('c://2.png', 'rb')}
                        files = {}
                        for key, value in self.body.items():
                            files[key] = open(value, 'rb')
                        self.res = requests.post(url=self.url, params=self.params,
                                                 cookies=self.cookies, headers=self.headers,
                                                 files=files)
                    else:
                        print("不支持的请求正文类型！")
                else:
                    self.res = requests.post(url=self.url, params=self.params,
                                             cookies=self.cookies, headers=self.headers)

            elif self.method == method.PUT:
                pass
                # requests.put()
            elif self.method == method.DELETE:
                pass
                # requests.delete()
            else:
                print("不支持的请求方法类型！")
        else:
            print("请求url不能为空！")

    @property
    def res_status_code(self):
        if self.res:
            return self.res.status_code
        else:
            print("响应内容为空，请检查响应情况！")

    @property
    def res_time(self):
        if self.res:
            return round(self.res.elapsed.total_seconds()*1000)
        else:
            print("响应内容为空，请检查响应情况！")

    @property
    def res_text(self):
        if self.res:
            return self.res.text
        else:
            print("响应内容为空，请检查响应情况！")

    @property
    def res_to_file(self):
        pass

    def res_html_parser(self, xpath, match_No=None):
        selector = etree.HTML(self.res_text)
        result = [e.text for e in selector.xpath(xpath)]
        if match_No is None:
            return result
        elif match_No == 0:
            return random.choice(result)
        elif match_No in range(0, len(result)+1):
            return result[match_No-1]
        else:
            print("索引无效！")

    #输入一个jsonpath返回一个 list
    def res_json_parser(self, json_path, match_No=None):
        try:
            json_dict = json.loads(self.res_text)
            result = jsonpath.jsonpath(json_dict, json_path)
            if result:
                if match_No is None:
                    return result
                elif match_No == 0:
                    return random.choice(result)
                elif match_No in range(0, len(result) + 1):
                    return result[match_No - 1]
                else:
                    print("索引无效！")
            else:
                print("json_path对应的节点，未找到！")
        except:
            print("响应json格式错误！")

   #输入一个jsonpath返回一个数值
    def res_json_parser_log(self, json_path):
        log = self.res_json_parser(json_path)
        log_key = None
        for i in log:
            log_key = i
        return log_key



    def res_xml_parser(self, xpath):
        et = ElementTree.fromstring(self.res_text)
        strings = et.findall(xpath)
        return strings


    #断言封装
    @unittest.expectedFailure
    def check_status_code(self, code=200):
        assert self.res_status_code, code
        print("check_status_code 【响应状态码pass】")


    def check_res_time_less_than(self, time=200):
        assert self.res_time <= time, True
        print("check_res_time 【pass】")


    @unittest.expectedFailure
     #"""判断数字返回结果与预期结果是否一致"""
    def check_res_text_contains(self, exp,text):
        assert exp == text, True
        print('响应内容错误：实际结果:{act}, 预期结果:{exp}'.format(
                act=exp, exp=text
            ))


    # 判断响应文本
    def check_res_text_equal(self, exp):
        assert self.res_text == exp, '响应内容错误：实际结果:{act}, 预期结果:{exp}'.format(
            act=self.res_text, exp=exp
        )


    def check_json_value(self, json_path, no, exp):
        assert self.res_json_parser(json_path, no), exp
        print("check_json_value 【pass】")

    def check_html_value(self, xpath, no, exp):
        assert self.res_html_parser(xpath, no), exp
        print("check_html_value 【pass】")
