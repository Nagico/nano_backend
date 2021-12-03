FROM python:3.8-buster

#定义容器的工作目录
WORKDIR /etc/uwsgi/nano_backend

#拷贝pip安装项目所需要的包名称和第三方django xadmin管理后台

ADD requirements.txt requirements.txt

#安装
RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

#开放的端口
EXPOSE 9000
