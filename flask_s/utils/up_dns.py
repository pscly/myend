import json
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models
from addict import Dict

def up_dns1(yuming1,yuming2, dns_id:int, dns_ip, dns_tokens:dict = {}, dns_type='A'):
    """ 
    api: https://cloud.tencent.com/document/product/1427/56157
    args :
        yuming1 : 域名 :pscly.cn
        yuming2 : 域名 :wc1
        dns_id : 例如 1178299063
        dns_ip : 例如 192.168.1.3
        dns_tokens: {
            "SecretId" : " ",
            "SecretKey" : " ",
            }
        dns_type : A 或者 CNAME
    域名对应:{
        'ny1':1214683704,
        'wc1':1178299063,
    }
    """
    if isinstance(dns_id, str):
        if dns_id.isdigit():
            dns_id = int(dns_id)
        else:
            dns_id = 1178299063
    dns_tokens = dns_tokens or os.y.data2
    dns_tokens = Dict(dns_tokens)
    print(dns_tokens)
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential(dns_tokens.get("CON_API1_SECRET_ID"), dns_tokens.get("CON_API1_SECRET_KEY"))
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "dnspod.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = dnspod_client.DnspodClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ModifyRecordRequest()
        params = {
            "Domain": yuming1,
            "SubDomain": yuming2,
            "RecordType": dns_type,
            "RecordLine": "默认",
            "Value": dns_ip,
            "RecordId": dns_id
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ModifyRecordResponse的实例，与请求对象对应
        resp = client.ModifyRecord(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
        
if __name__ == '__main__':
    os.y = Dict()
    os.y.data2 = {
        "CON_API1_SECRET_ID": "x",
        "CON_API1_SECRET_KEY": "x",
    }
    x = up_dns1('pscly.cn','wc1',1178299063,'192.168.31.11')
    print(x)
