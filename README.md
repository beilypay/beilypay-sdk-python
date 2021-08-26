# Beilypay SDK Python v2.0.1 RELEASE 2021-08-24


## 一、注意
   - 我们提供的代码仅供参考，在确定符合使用场景、代码质量的情况下，酌情参考使用。
   - 测试环境 apiHost 为 http://dev.beilypay.com
   - 生产环境 apiHost 为 http://service.beilypay.com
   - 测试对接参数，详见 test.py


## 二、引入库

```python
from beilypay import Beilypay
from exceptions import BeilyException
```

## 三、构造SDK对象

```python
beily = Beilypay("1183601355", 3, "8c62bd95169ba8818c676a6f2025b8e5", "http://dev.beilypay.com")
```

## 四、代收和查询
```python
try:
  order = beily.createPayment(str(random.randint(100000000, 999999999999)), "111", "http://www.baidu.com/", "http://www.baidu.com/", "userId111", "userName111" )
  print("orderNo: " + order['orderNo'])
  print("payUrl: " + order['payUrl'])
  print("create payment order: " + str(order))
  
  orderNo = order["orderNo"]
  order2 = beily.queryPayment(orderNo)
  print("query payment order: " + str(order))  
except BeilyException as e:
  print(e)
except Exception as e2:
  print(e2)
```

## 五、代付和查询
```python
try: 
  order = beily.createTrans(str(random.randint(100000000, 999999999999)), 123, "http://www.baidu.com/notifyUrl", "Card", "account", "owner", "bankcode", "ifsc", "this is address")
  print("create trans order: " + str(order))

  orderNo = order["orderNo"]
  order2 = beily.queryTrans(orderNo)
  print("query trans order: " + str(order))
except BeilyException as e:
  print(e)
except Exception as e2:
  print(e2)
```