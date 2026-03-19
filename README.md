# 学生宿舍管理控制系统

---

## 项目结构

```
StudenManager/
├── ManagerApi/                   # 后端Django项目
│   ├── ManagerApi/               # 项目配置目录
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings/            # 配置文件目录
│   │   │   ├── __init__.py
│   │   │   └── dev.py           # 开发环境配置
│   │   ├── urls.py              # 项目URL配置
│   │   └── wsgi.py
│   ├── apps/                    # Django应用目录
│   │   ├── __init__.py
│   │   └── users/               # 用户管理应用
│   │       ├── __init__.py
│   │       ├── admin.py         # 后台管理配置
│   │       ├── apps.py          # 应用配置
│   │       ├── filters.py       # 过滤功能
│   │       ├── migrations/      # 数据库迁移文件
│   │       ├── models.py        # 数据模型
│   │       ├── serializer.py    # 数据序列化器
│   │       ├── tests.py         # 测试文件
│   │       ├── urls.py          # 应用URL配置
│   │       └── views.py         # 视图函数
│   ├── logs/                    # 日志目录
│   │   └── sm.log               # 系统日志文件
│   ├── uploads/                 # 上传文件目录
│   └── manage.py                # Django管理脚本
├── manager-vue/                  # 前端Vue项目
│   ├── public/                   # 静态资源
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── staticImg/           # 图片资源
│   │   └── staticVoid/          # 视频资源
│   ├── src/                     # 源代码
│   │   ├── assets/              # 项目资源
│   │   ├── components/          # Vue组件
│   │   │   ├── Admin.vue        # 管理员主组件
│   │   │   ├── AdminComp/       # 管理员子组件
│   │   │   │   ├── FloorManage.vue   # 楼层管理组件
│   │   │   │   ├── HanderComp.vue    # 处理组件
│   │   │   │   └── HostelManage.vue  # 宿舍管理组件
│   │   │   ├── Login.vue        # 登录组件
│   │   │   ├── Students.vue     # 学生端组件
│   │   │   └── Teachers.vue     # 教师端组件
│   │   ├── routers/             # 路由配置
│   │   ├── App.vue              # 根组件
│   │   ├── main.js              # 入口文件
│   │   └── settings.js          # 配置文件
│   ├── .gitignore
│   ├── README.md
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   └── vue.config.js
├── README.md                    # 项目说明文档
├── environment.txt              # Python依赖文件
├── LICENSE                      # 许可证文件
└── venv/                        # Python虚拟环境 (可选)
```
