import requests

def get_ip_location(ip_address):
    try:
        # 来源 https://opendata.baidu.com/api.php?co=&resource_id=6006&oe=utf8&query=121.8.215.106
        # https://opendata.baidu.com/api.php?co=&resource_id=6006&oe=utf8&query=121.8.215.106
        """
        {
            "status": "0",
            "t": "",
            "set_cache_time": "",
            "data": [
                {
                    "ExtendedLocation": "",
                    "OriginQuery": "121.8.215.106",
                    "SchemaVer": "",
                    "appinfo": "",
                    "disp_type": 0,
                    "fetchkey": "121.8.215.106",
                    "location": "广东省广州市 电信",
                    "origip": "121.8.215.106",
                    "origipquery": "121.8.215.106",
                    "resourceid": "6006",
                    "role_id": 0,
                    "schemaID": "",
                    "shareImage": 1,
                    "showLikeShare": 1,
                    "showlamp": "1",
                    "strategyData": {},
                    "titlecont": "IP地址查询",
                    "tplt": "ip"
                }
            ]
        }
        """
        response = requests.get(f"https://opendata.baidu.com/api.php?co=&resource_id=6006&oe=utf8&query={ip_address}")
        data = response.json()
        return f"{data.get('data', [{}])[0].get('location', 'Unknown')}"
    except:
        return "Unknown"

