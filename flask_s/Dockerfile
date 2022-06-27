FROM python:3.10

# 更改时区
ENV TIME_ZONE=Asia/Shanghai \
    PIPURL="https://mirrors.aliyun.com/pypi/simple/"

RUN rm -rf /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security buster/updates main" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian-security buster/updates main" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib" >> /etc/apt/sources.list && \
    apt-get -y update && apt-get -y upgrade && \
    rm -rf /root/.cache && apt-get autoclean && \
    rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/* && \
    echo ${TIME_ZONE} > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

WORKDIR /py_end

# COPY ./requirements.txt requirements.txt
# 安装pip包
# RUN pip3 install pdm
RUN pip3 install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
# RUN pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/            

