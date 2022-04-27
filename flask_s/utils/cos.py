# coding=utf-8
import logging
import sys
import time

from qcloud_cos import CosConfig, CosS3Client
from pprint import pprint

# from . import factory


class Cos():
    def __init__(self, config_y: dict):
        # 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
        token = None
        scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

        self.config1 = config_y
        self.config = CosConfig(Region=config_y.get('region'), SecretId=config_y.get('secret_id'),
                                SecretKey=config_y.get('secret_key'), Token=token, Scheme=scheme)
        self.client = CosS3Client(self.config)

    def upload_file(self, bucket_name, local_path, remote_path):
        self.client.upload_file(bucket_name, local_path, remote_path)
        return True

    def upload_file2(self, Bucket, File_name, File_2, PartSize=1, MAXThread=5, EnableMD5=False, progress_callback=None,
                     **kwargs):
        """
        将此处源代码进行重写, 上传的就是2进制文件，而不是文件地址
        分块代码已经被我去掉了，因为我发送的文件都是2进制文件，不需要分块，也不应该分块
        
        args:
            

        .. code-block:: python

            config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
            client = CosS3Client(config)
            # 根据文件大小自动选择分块大小,多线程并发上传提高上传速度
            file_name = 'thread_1GB_test'
            response = client.upload_file(
                Bucket='bucket',
                Key=file_name,
                File_2=file_name,
                PartSize=10,
                MAXThread=10,
            )
        """
        return self.client.put_object(Bucket=Bucket, Key=File_name,
                                      Body=File_2, EnableMD5=EnableMD5, **kwargs)

    def get_files(self, bucket_name: str, prefix: str = '', limit: int = 1000, offset: int = 0):
        """
        返回存储桶中的文件列表
        args:
            bucket_name: 存储桶名称
            prefix: 查询的文件夹，可以不要
            limit: 每次返回的文件数量，默认为1000
            offset: 偏移量，默认为0, 即从第一个文件开始
        """
        self.response = self.client.list_objects(
            Bucket=bucket_name)    # prefix是指查询的文件夹，可以不填
        # response = client.list_objects(Bucket=config.get('bucket'), Prefix=config.get('prefix'))    # prefix是指查询的文件夹，可以不填
        r_list = []
        if 'Contents' in self.response:
            for content in self.response['Contents']:
                file_data = {
                    'file_name': content['Key'],
                    'file_size': content['Size'],
                    'file_time': time.mktime(time.strptime(content['LastModified'][:-5], "%Y-%m-%dT%H:%M:%S")),
                    'file_url': self.config1.get('COS_CDN') + content['Key']
                }
                r_list.append(file_data)
        r_list.sort(key=lambda x: x['file_time'], reverse=True)
        return r_list


if __name__ == '__main__':
    config = {}
    c = Cos(config)

    # with open(r'‪C:\Users\pscly\Videos\2022-03-13 11-46-52.mkv')
    # with open(r'C:\Users\pscly\Desktop\t1\b (5).txt', 'rb') as f:
    #     file_d = f.read()
    # x = c.upload_file2(config['Bucket'], Key='a/b/b.txt', File_2=file_d)
    x = c.get_files(config['Bucket'])
    pprint(x)
