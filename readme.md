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
   
### 使用 uv 本地运行

```bash
cd flask_s
uv sync
uv run python app.py
```

也可以直接运行脚本：

```bash
./flask_s/run.sh
```


## TODO

1. 考虑补充开放API文档
2. 加密解密功能也整个接口出来试试
