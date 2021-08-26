 # -*- coding:utf-8 -*-

import sys
import json
import http.client
import random
from beilypay import Beilypay
from exceptions import BeilyException
 
# beily = Beilypay("1183601355", 3, "8c62bd95169ba8818c676a6f2025b8e5", "http://dev.beilypay.com")
# try:
#   order = beily.createPayment(str(random.randint(100000000, 999999999999)), "111", "http://www.baidu.com/", "http://www.baidu.com/", "userId111", "userName111" )
#   print("orderNo: " + order['orderNo'])
#   print("payUrl: " + order['payUrl'])
#   print("create payment order: " + str(order))
  
#   orderNo = order["orderNo"]
#   order2 = beily.queryPayment(orderNo)
#   print("query payment order: " + str(order))  
# except BeilyException as e:
#   print(e)
# except Exception as e2:
#   print(e2)

# try: 
#   order = beily.createTrans(str(random.randint(100000000, 999999999999)), 123, "http://www.baidu.com/notifyUrl", "Card", "account", "owner", "bankcode", "ifsc", "this is address")
#   print("create trans order: " + str(order))

#   orderNo = order["orderNo"]
#   order2 = beily.queryTrans(orderNo)
#   print("query trans order: " + str(order))
# except BeilyException as e:
#   print(e)
# except Exception as e2:
#   print(e2)