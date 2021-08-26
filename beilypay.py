 # -*- coding:utf-8 -*-

import collections
import hashlib
import json
import http.client
import random
import urllib.parse
from exceptions import BeilyException

class Beilypay:

  __appId = ""
  __merchanId = ""
  __appSecret = ""
  __apiHost = ""

  # --------------
  # 构造方法  
  # --------------
  def __init__(self, 
      appId,        # 商户 APPID
      merchanId,    # 商户号
      appSecret,    # 商户密钥
      apiHost       # 对接 api 的地址，以 http 或 https 开头
  ):
    self.__appId = appId
    self.__merchanId = merchanId
    self.__appSecret = appSecret
    self.__apiHost = apiHost.rstrip("/") + "/v2"
    if not self.__apiHost.startswith("http"):
      self.__apiHost = "http://" + self.__apiHost

  # --------------
  # 签名计算函数
  # --------------
  def sign(self, data):
    data = sorted(data)

    _str = ""
    for k,v in data:
      _str += k + "=" + str(v) + "&"
    _str += "key=" + self.__appSecret
    m = hashlib.md5()
    m.update(bytes(_str, "UTF-8"))
    return m.hexdigest()

  # --------------
  # 创建代收订单
  # **建议** 引导用户填写真实 的手机号，可以兼容更多的支付平台
  # --------------
  def createPayment(self, 
      outOrderNo,       # 商户订单号
      amount,           # 订单金额
      notifyUrl,        # 订单回调地址（支付成功才有回调）
      frontCallback,    # 前端页面回跳地址
      userId,           # 商户的用户ID
      userName,         # 商户的用户昵称
      mobile = "",      # 商户的用户手机号，留空 则 默认随机10位数字，**建议** 引导用户填写真实 的手机号，可以兼容更多的支付平台
      email = ""        # 商户的用户Email地址，留空 则 {$mobile}@gmail.com
  ):
    if mobile == "":
      for i in range(0, 9):
        mobile = str(random.randint(1000000000, 9999999999))
    if email == "":
      email = mobile + '@gmail.com'


    request = collections.OrderedDict()
    request["appId"]          = self.__appId
    request["merchantId"]     = self.__merchanId
    request["payAmount"]      = amount
    request["mobile"]         = mobile
    request["email"]          = email
    request["notifyUrl"]      = notifyUrl
    request["frontCallback"]  = frontCallback
    request["outOrderNo"]     = outOrderNo
    request["userId"]         = userId
    request["userName"]       = userName
    request["sign"]           = self.sign(request.items())

    jsonstr = json.dumps( request )
    _url = urllib.parse.urlparse(self.__apiHost)
    conn = http.client.HTTPConnection(_url.hostname, _url.port)
    headers = {"Content-Type": "application/json"}
    conn.request("POST", self.__apiHost + '/payment/create', bytes(jsonstr, 'UTF-8'), headers)
    res = conn.getresponse()
    resp = json.loads( str(res.read(), "UTF-8") )
    if resp["code"] == 200:
      return resp["data"]

    raise BeilyException(resp["code"], resp["msg"])

  # --------------
  # 创建代付订单  
  # **建议** 引导用户填写真实 的手机号，可以兼容更多的支付平台
  # --------------
  def createTrans(self,
      orderNumber,    # 商户的订单号
      amount,         # 代付金额
      notifyUrl,      # 代付结果回调地址
      accountType,    # 收款账户类型 Card: 代付到银行卡
      account,        # 对应的收款账户
      accountOwner,   # 账户持有者姓名
      bankCode,       # 账户类型为Card,对应的银行编码
      ifsc,           # 账户类型为Card,分行的IFSC代码	
      address = "",   # 收款人地址
      mobile = "",    # 收款人手机号 留空 则 默认随机10位数字, **建议** 引导用户填写真实 的手机号，可以兼容更多的支付平台
      email = ""      # 收款人邮箱 留空 则 {$mobile}@gmail.com
  ):
    if mobile == "":
      for i in range(0, 9):
        mobile = str(random.randint(1000000000, 9999999999))
    if email == "":
      email = mobile + '@gmail.com'

    request = {
        "appId"         : self.__appId,
        "merchantId"    : self.__merchanId,
        "notifyUrl"     : notifyUrl,
        "outOrderNo"    : orderNumber,
        "payAmount"     : amount,
        "accountType"   : accountType,
        "account"       : account,
        "accountOwner"  : accountOwner,
        "bankCode"      : bankCode,
        "ifsc"          : ifsc,
        "address"       : address,
        "mobile"        : mobile,
        "email"         : email
    }
    request["sign"] = self.sign(request.items())
    jsonstr = json.dumps( request )
    _url = urllib.parse.urlparse(self.__apiHost)
    conn = http.client.HTTPConnection(_url.hostname, _url.port)
    headers = {"Content-Type": "application/json"}
    conn.request("POST", self.__apiHost + '/trans/create', bytes(jsonstr, 'UTF-8'), headers)
    res = conn.getresponse()
    resp = json.loads( str(res.read(), "UTF-8") )
    if resp["code"] == 200:
      return resp["data"]

    raise BeilyException(resp["code"], resp["msg"])

  # --------------
  # 查询代收订单
  # --------------
  def queryPayment(self, orderNo):
    request = {
        "appId"         : self.__appId,
        "merchantId"    : self.__merchanId,
        "orderNo"       : orderNo,
    }
    request["sign"] = self.sign(request.items())
    jsonstr = json.dumps( request )
    _url = urllib.parse.urlparse(self.__apiHost)
    conn = http.client.HTTPConnection(_url.hostname, _url.port)
    headers = {"Content-Type": "application/json"}
    conn.request("POST", self.__apiHost + '/payment/query', bytes(jsonstr, 'UTF-8'), headers)
    res = conn.getresponse()
    resp = json.loads( str(res.read(), "UTF-8") )
    if resp["code"] == 200:
      return resp["data"]

    raise BeilyException(resp["code"], resp["msg"])


  # --------------
  # 查询代付订单
  # --------------
  def queryTrans(self, orderNo):
    request = {
        "appId"         : self.__appId,
        "merchantId"    : self.__merchanId,
        "orderNo"       : orderNo,
    }
    request["sign"] = self.sign(request.items())
    jsonstr = json.dumps( request )
    _url = urllib.parse.urlparse(self.__apiHost)
    conn = http.client.HTTPConnection(_url.hostname, _url.port)
    headers = {"Content-Type": "application/json"}
    conn.request("POST", self.__apiHost + '/trans/query', bytes(jsonstr, 'UTF-8'), headers)
    res = conn.getresponse()
    resp = json.loads( str(res.read(), "UTF-8") )
    if resp["code"] == 200:
      return resp["data"]

    raise BeilyException(resp["code"], resp["msg"])