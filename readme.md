#  简介

这个东西是为了让我的后端能够更好的使用
(emmmm. 才发现end不是后的意思，是结束的意思，我这库名多少有点离谱)

## 运行

1. 安装python
2. pip install -r requirements.txt
3. python app.py

## 功能

1. 通过接受请求，来将ip写入数据库，或者文件中，让我能够进行ip地址查看，或者是其他情况
    1. header 中的参数
       1. is_y: 必须, 而且是1
       2. who: 可选 我是谁

## 问题

- [ ] 直接把数据库的密码上传过去不太好吧
  - [ ] 1. IP地址使用腾讯的内网地址
  - [ ] 2. 代码库使用我的gitea平台，而不是github

## TODO 
- [ ] 得把IP数据写入到数据库中
  - [ ] 如何写入呢？
    - [ ] 环境变量配置策略
    - [ ] 本地直接docker部署一个数据库
    - [ ] 云服务器的内网来连接数据库

