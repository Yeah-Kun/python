# 成绩查询项目
## 简介
替某非营利机构做的成绩查询系统，主要实现学生在移动端查询成绩，管理员在后台对成绩进行增删查改。
## 开发环境
- Python 3.6.0
- Django 1.11.4
- Mysqlclient 1.3.10

## 概念

### MTV模式（Model Template View）

- Model(模型)：负责业务对象与数据库的对象(ORM)
- Template(模版)：负责如何把页面展示给用户
- View(视图)：负责业务逻辑，并在适当的时候调用Model和Template


---
### 启动服务
- 点击 RunServer.bat 可启动服务。目前设置的发布端口为 8000,可在 RunServer.bat 中进行更改
- 本机启动服务后，浏览器输入：http://127.0.0.1:8000/ 进行查分访问
- 本机启动服务后，浏览器输入：http://127.0.0.1:8000/admin 进行后台访问

### 后台账号密码
与未迁移代码的设置一致

### 合并过程修改的内容
- 根据Django的MTV模式，重构了部分代码
- 使用了新的数据库，避免在操作数据时的冲突
- 模型层（models.py）的命名改成小写+下划线
- 使用了命名空间和模板语言，方便修改

### 目录树

```
│  manage.py
│
├─mainsite 
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  |__init__.py
│
├─srsys
│  │  admin.py
│  │  apps.py
│  │  models.py # 模型层，原mysqldb模型层整合到这里
│  │  tests.py
│  │  urls.py
│  │  views.py  # 业务逻辑层，整合了login.py
│  │  __init__.py
│  │
│  ├─migrations
│  │  │  0001_initial.py
│  │  │  __init__.py
│  ├─templates   # 应用级的模板层
│     └─srsys
│             index.html  # 查询页面
│             result.html # 成绩单
│
└─templates
    │  index.html
    │  result.html
    │
    └─admin
            base_site.html
```

### 日志
- 迁移代码，实现用户基本查询，后台的增删查改功能（2017-8-14）

### BUG
