# 学生宿舍管理控制系统

---

## 📖 项目简介

智慧宿舍一体化管理平台是一个集信息管理、出入控制、数据分析于一体的综合性系统。它创新性地将线上管理系统与线下ID卡门禁硬件打通，形成了完整的管理闭环，为高校宿舍管理提供了高效、安全、便捷的全新体验。

### ✨ 核心亮点

-   **🔗 软硬一体化**：无缝集成ID身份卡与刷卡软件，实现学生出入记录的自动化管理与实时监控。
-   **🏗️ 前后端分离**：采用现代化的前后端分离架构，前端负责交互，后端提供API，开发效率高，可维护性强。
-   **👥 多角色支持**：精细化设计学生、教师（辅导员）、管理员三种角色，权限分明，功能各异。
-   **📊 数据可视化**：提供数据可视化大屏，动态展示宿舍入住率、报修统计等关键指标，辅助管理决策。
-   **🚀 全流程覆盖**：从宿舍分配、入住管理到日常报修、出入记录，覆盖宿舍管理核心业务流程。

---

## 技术栈

### 前端技术
- **框架**: Vue.js 2.6.14
- **UI组件库**: Element UI 2.15.14
- **路由管理**: Vue Router 3.6.5
- **构建工具**: Vue CLI
- **HTTP客户端**: Axios

### 后端技术
- **Web框架**: Django 5.2.8
- **API框架**: Django REST Framework
- **数据库**: SQLite (开发环境)
- **ORM**: Django ORM
- **API设计**: RESTful API

### 开发环境
- **Python**: 3.13
- **Node.js**: 14.x 或更高版本
- **数据库**: SQLite (开发环境)
- **操作系统**: Windows/Linux/MacOS

## 系统架构
- **前后端分离架构**
- **前端**: SPA (Single Page Application) 单页应用
- **后端**: Django REST API服务
- **数据通信**: HTTP请求/响应
- **认证机制**: 基于Token的身份认证
- **权限控制**: 基于角色的访问控制 (RBAC)

## 功能模块

### 1. 用户认证系统
- 统一登录入口，支持学生、教师、管理者三种角色登录
- 账号密码验证登录
- 角色权限管理
- 基于Token的身份认证机制

### 2. 宿舍信息管理 (管理员)
- 宿舍基本信息维护（编号、性别、容量等）
- 宿舍信息查询与统计
- 宿舍删除功能（含确认对话框）

### 3. 楼层管理 (管理员)
- 楼层信息维护
- 楼层与房间关联管理
- 楼层删除功能（含确认对话框）

### 4. 学生管理
- **学生端**: 个人信息查看、宿舍信息查看
- **管理员端**: 学生信息登记、学生删除功能（含确认对话框）、学生分配宿舍

### 5. 教师功能
- 教师角色特定功能（待完善）

### 6. 数据展示
- 楼层信息列表展示
- 宿舍信息列表展示
- 学生信息列表展示
- 分页功能支持

## 快速开始

### 前端环境配置

```bash
# 进入前端项目目录
cd manager-vue

# 安装依赖
npm install

# 开发环境运行 (默认端口: 8080)
npm run serve

# 构建生产版本
npm run build
```

### 后端环境配置

```bash
# 进入后端项目目录
cd ManagerApi

# 创建虚拟环境（可选但推荐）
python -m venv venv

# 激活虚拟环境
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 安装依赖
pip install -r environment.txt

# 运行数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器 (默认端口: 8000)
python manage.py runserver
```

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

## API文档
系统使用Django REST Framework提供RESTful API，主要API端点包括：

### 用户相关API
- `POST /api/login/` - 用户登录
- `POST /api/logout/` - 用户登出

### 宿舍相关API
- `GET /api/hostels/` - 获取宿舍列表
- `POST /api/hostels/` - 创建新宿舍
- `GET /api/hostels/<id>/` - 获取单个宿舍信息
- `PUT /api/hostels/<id>/` - 更新宿舍信息
- `DELETE /api/hostels/<id>/` - 删除宿舍

### 楼层相关API
- `GET /api/floors/` - 获取楼层列表
- `POST /api/floors/` - 创建新楼层
- `GET /api/floors/<id>/` - 获取单个楼层信息
- `PUT /api/floors/<id>/` - 更新楼层信息
- `DELETE /api/floors/<id>/` - 删除楼层

### 学生相关API
- `GET /api/students/` - 获取学生列表
- `POST /api/students/` - 创建新学生
- `GET /api/students/<id>/` - 获取单个学生信息
- `PUT /api/students/<id>/` - 更新学生信息
- `DELETE /api/students/<id>/` - 删除学生

*详细API文档可通过Django REST Framework的自动生成文档查看：http://localhost:8000/docs/*

## 注意事项
1. **环境配置**: 确保Node.js (14.x+) 和 Python (3.13+) 版本符合要求
2. **前端配置**: 前端默认连接到后端地址 `http://127.0.0.1:8000`，可在 `src/settings.js` 中修改
3. **数据库初始化**: 首次使用需要运行数据库迁移并创建超级用户
4. **安全配置**: 生产环境部署前需要：
   - 修改 `ManagerApi/ManagerApi/settings/dev.py` 中的SECRET_KEY
   - 配置HTTPS
   - 设置合适的CORS策略
   - 配置生产环境数据库
5. **删除功能**: 系统中的删除操作（删除宿舍、学生、楼层）都有确认对话框，防止误操作
6. **权限管理**: 不同角色有不同的操作权限，确保正确配置用户角色

## 待开发功能
1. **水电费管理模块**: 实现水电费数据录入、查询和统计功能
2. **报修管理模块**: 实现报修申请、进度跟踪和维修记录管理
3. **公告通知模块**: 实现系统公告发布和通知消息管理
4. **数据统计功能**: 添加数据统计和图表展示功能
5. **消息推送系统**: 集成消息推送功能
6. **移动端适配**: 优化移动端界面和用户体验
7. **导出功能**: 添加数据导出（Excel/PDF）功能
8. **打印功能**: 支持宿舍分配表等文档打印

## 贡献指南
1. Fork 本项目
2. 创建新的特性分支 (`git checkout -b feature/xxx`)
3. 提交代码变更 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

## 许可证
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式
- 项目负责人: [Sky_Oblivion]
- 电子邮件: [2014567412@qq.com]
- 项目地址: [https://gitee.com/spidermanehe/students-manager]

---

*注：本项目为大学本科毕业设计作品，持续开发和完善中。*