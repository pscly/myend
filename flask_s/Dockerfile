# 这玩意的路径是当前文件的路径，而不是项目的根路径(不是dockeryaml的路径)
# 重新构建 > docker build .
FROM python:3.9

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /py_end

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=31001
ENV FLASK_ENV=production

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# CMD [ "python3", "app.py" ]
CMD ["flask", "run"]
