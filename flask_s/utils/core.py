import os
import requests
import re
import yaml
import json
import time


def is_file(path):
    return os.path.isfile(path)


def load_config_yaml(path='config/config.yaml', mode='WAI', err=True):
    if not is_file(path):
        if err:
            raise Exception(f'{path}文件不存在')
        return {}
    return yaml.safe_load(open(path, 'r'))[mode]


def load_json(path='config/config.json'):
    if is_file(path):
        raise Exception(f'{path}文件不存在')
    return json.load(open(path, 'r'))


class MyRes():
    '''
    封装一个获取结果的类
    仔细想想， 可以把cookies保存到一个对象中，到时候获取和调用都很方便了
    '''

    def __init__(self, config: dict, headers={}, cookies={}, coding='gb2312') -> None:
        self.config = config
        self.headers = headers
        self.cookies = cookies
        self.coding = coding
        self.xueqi = '0'
        self.xh = ''
        self.pwd = ''
        self.name = ''
        self.url = ''

    def get_res(self, url, re_text=None, params={}):
        '''
        封装requests.get方法
        args:
            url: 访问地址
            re_text: 可选，提供正则，自动匹配
            headers: 可选，自己提供一个headers

        return: res1, re后的东西
        返回res1，想要什么就拿什么
        '''
        url = self.config['JWJC_URL'] + url
        res1 = requests.get(url, cookies=self.cookies, params=params)
        res1.encoding = self.coding
        self.cookies.update(res1.cookies.get_dict())
        self.url = url
        self.headers = res1.headers
        self.headers['Referer'] = url
        self.text = res1.text
        self.res1 = res1
        if re_text:
            re_hou = re.findall(re_text, res1.text)
            return res1, re_hou
        return res1, None

    def post_res(self, url, data, re_text=None):
        '''
        封装requests.post方法
        '''
        url = self.config['JWJC_URL'] + url
        res1 = requests.post(
            url, data=data, cookies=self.cookies)  # 这里加上header就有问题
        res1.url = self.url
        res1.encoding = self.coding
        self.cookies.update(res1.cookies.get_dict())
        # self.headers = res1.headers
        self.headers['Referer'] = url
        self.res1 = res1
        if re_text:
            re_hou = re.findall(re_text, res1.text)
            return res1, re_hou
        return res1, None


def get_files(path):
    """
    将目录下的所有非y_的文件名，返回一个列表，通过文件的创建时间排序
    """
    if not os.path.isdir(path):
        os.system(f"mkdir -p {path}")
    files_path = os.listdir(path)
    files = [file for file in files_path if not file.startswith('y_')]
    files_dates = [os.path.getmtime(os.path.join(path, file))
                   for file in files]
    t_files = list(
        zip(
            [time.strftime("%Y-%m-%d %X", time.localtime(files_date))
                           for files_date in files_dates],
            files,
            files_dates,
        )
    )
    t_files.sort(key=lambda x: x[2], reverse=True)
    return t_files
