#  简介

此项目是集大家于一身的项目
实现功能:

1. 模拟共享网盘系统
2. 后端专用接口模拟
3. 文本加密签名验证
4. 集成自动化 DDNS 

## 运行

### 使用docker

1. docker-compose up -d
   
### 使用python

### 使用原生python运行

```bash
cd flask_s
python3 install -r ./requirements.txt
python3 app.py 0.0.0.0:80
```

#### 使用pdm (python虚拟环境管理运行)

```
cd flask_s
pdm update
pdm run start
```


## TODO

1. 考虑补充开放API文档
