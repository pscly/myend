# 简介

## toc

1. [简介](#简介)
   1. [数据库迁移](#数据库迁移)
   2. [关于支付模块](#关于支付模块)
      1. [发起支付请求](#发起支付请求)
      2. [支付请求1](#支付请求1)
   3. [发起支付请求](#发起支付请求-1)
   4. [支付请求2](#支付请求2)
   5. [发起支付请求](#发起支付请求-2)

## 数据库迁移

初始化，创建 alembic 文件夹(现在不用这个)  (这个似乎非得要用那个ini文件, 但是修改env.py 后似乎就可以不用了)
alembic init alembic

初始化
alembic upgrade head 

生成迁移脚本
alembic revision --autogenerate -m "init db"

应用迁移到数据库
alembic upgrade head

后续更新
alembic revision --autogenerate -m "update db"
alembic upgrade head



## 关于支付模块

发起支付请求
URL地址：//url_pay/submit.php?pid={商户ID}&type={支付方式}&out_trade_no={商户订单号}&notify_url={服务器异步通知地址}&return_url={页面跳转通知地址}&name={商品名称}&money={金额}&sitename={网站名称}&sign={签名字符串}&sign_type=MD5

发起支付请求
URL地址：//url_pay/api.php?pid={商户ID}&type={支付方式}&out_trade_no={商户订单号}&notify_url={服务器异步通知地址}&return_url={页面跳转通知地址}&name={商品名称}&money={金额}&sitename={网站名称}&sign={签名字符串}&sign_type=MD5

URL地址：//url_pay/api.php?pid={商户ID}&type={支付方式}&out_trade_no={商户订单号}&notify_url={服务器异步通知地址}&return_url={页面跳转通知地址}&name={商品名称}&money={金额}&sitename={网站名称}&sign={签名字符串}&sign_type=MD5

### 发起支付请求

```
payurl/submit.php?pid={商户ID}&type={支付方式}&out_trade_no={商户订单号}&notify_url={服务器异步通知地址}&return_url={页面跳转通知地址}&name={商品名称}&money={金额}&sitename={网站名称}&sign={签名字符串}&sign_type=MD5
```

请求参数说明：

### 支付请求1

## 发起支付请求

URL地址：//url_pay/api.php?pid={商户ID}&type={支付方式}&out_trade_no={商户订单号}&notify_url={服务器异步通知地址}&return_url={页面跳转通知地址}&name={商品名称}&money={金额}&sitename={网站名称}&sign={签名字符串}&sign_type=MD5

请求参数说明：

| 字段名       | 变量名       | 必填 | 类型   | 示例值                           | 描述                                                                                                                                                                                                       |
| ------------ | ------------ | ---- | ------ | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 商户ID       | pid          | 是   | Int    | 1001                             |                                                                                                                                                                                                            |
| 支付方式     | type         | 是   | String | alipay                           | alipay:支付宝,tenpay:财付通,``qqpay:QQ钱包,wxpay:微信支付                                                                                                                                                  |
| 商户订单号   | out_trade_no | 是   | String | 20160806151343349                |                                                                                                                                                                                                            |
| 异步通知地址 | notify_url   | 是   | String | //www.cccyun.cc/notify_url.php   | 服务器异步通知地址                                                                                                                                                                                         |
| 跳转通知地址 | return_url   | 是   | String | //www.cccyun.cc/return_url.php   | 页面跳转通知地址                                                                                                                                                                                           |
| 商品名称     | name         | 是   | String | VIP会员                          |                                                                                                                                                                                                            |
| 商品金额     | money        | 是   | String | 1.00                             |                                                                                                                                                                                                            |
| 网站名称     | sitename     | 否   | String | 彩虹云任务                       |                                                                                                                                                                                                            |
| 签名字符串   | sign         | 是   | String | 202cb962ac59075b964b07152d234b70 | 签名算法与支付宝签名算法相同``(money={商品金额}&name={商品名称}& notify_url={异步通知地址}&out_trade_no={商户订单号}&pid={商户ID}&return_url={同步通知地址}&sitename={站点名称}&type={支付方式}{商户密匙}) |
| 签名类型     | sign_type    | 是   | String | MD5                              | 默认为MD5                                                                                                                                                                                                  |

## 支付请求2



## 发起支付请求

URL地址：//url_pay/submit.php?pid={商户ID}&type={支付方式}&out_trade_no={商户订单号}&notify_url={服务器异步通知地址}&return_url={页面跳转通知地址}&name={商品名称}&money={金额}&sitename={网站名称}&sign={签名字符串}&sign_type=MD5

请求参数说明：

| 字段名       | 变量名       | 必填 | 类型   | 示例值                           | 描述                                                                                                                                                                                                       |
| ------------ | ------------ | ---- | ------ | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 商户ID       | pid          | 是   | Int    | 1001                             |                                                                                                                                                                                                            |
| 支付方式     | type         | 是   | String | alipay                           | alipay:支付宝,tenpay:财付通,``qqpay:QQ钱包,wxpay:微信支付                                                                                                                                                  |
| 商户订单号   | out_trade_no | 是   | String | 20160806151343349                |                                                                                                                                                                                                            |
| 异步通知地址 | notify_url   | 是   | String | //www.cccyun.cc/notify_url.php   | 服务器异步通知地址                                                                                                                                                                                         |
| 跳转通知地址 | return_url   | 是   | String | //www.cccyun.cc/return_url.php   | 页面跳转通知地址                                                                                                                                                                                           |
| 商品名称     | name         | 是   | String | VIP会员                          |                                                                                                                                                                                                            |
| 商品金额     | money        | 是   | String | 1.00                             |                                                                                                                                                                                                            |
| 网站名称     | sitename     | 否   | String | 彩虹云任务                       |                                                                                                                                                                                                            |
| 签名字符串   | sign         | 是   | String | 202cb962ac59075b964b07152d234b70 | 签名算法与支付宝签名算法相同``(money={商品金额}&name={商品名称}& notify_url={异步通知地址}&out_trade_no={商户订单号}&pid={商户ID}&return_url={同步通知地址}&sitename={站点名称}&type={支付方式}{商户密匙}) |
| 签名类型     | sign_type    | 是   | String | MD5                              | 默认为MD5                                                                                                                                                                                                  |
