# 学生宿舍管理控制系统

## 项目介绍
本项目是一个学生宿舍管理控制系统，为大学本科毕业设计作品。系统旨在提供高效、便捷的宿舍管理解决方案，支持学生、教师和管理者三种角色的用户登录和操作，实现宿舍信息管理、学生入住管理、水电费管理等功能。

## 技术栈

### 前端技术
- **框架**: Vue.js 2.6.14
- **UI组件库**: Element UI 2.15.14
- **路由管理**: Vue Router 3.6.5
- **构建工具**: Vue CLI

### 后端技术
- **Web框架**: Django 5.2.8
- **数据库**: SQLite (开发环境)
- **API设计**: RESTful API

## 系统架构
- **前后端分离架构**
- **前端**: SPA (Single Page Application) 单页应用
- **后端**: Django REST API服务
- **数据通信**: HTTP请求/响应

## 功能模块

### 1. 用户认证系统
- 统一登录入口，支持学生、教师、管理者三种角色登录
- 账号密码验证登录
- 角色权限管理

### 2. 宿舍信息管理
- 宿舍基本信息维护
- 楼层与房间信息管理
- 房间状态监控

### 3. 学生入住管理
- 学生信息登记
- 入住与退房管理
- 宿舍分配与调整

### 4. 水电费管理
- 水电费数据录入
- 费用查询与统计
- 缴费记录管理

### 5. 报修管理
- 报修申请提交
- 报修进度跟踪
- 维修记录管理

### 6. 公告通知
- 发布系统公告
- 通知消息管理
- 重要信息展示

## 快速开始

### 前端环境配置

```bash
# 进入前端项目目录
cd manager-vue

# 安装依赖
npm install

# 开发环境运行
npm run serve

# 构建生产版本
npm run build
```

### 后端环境配置

```bash
# 进入后端项目目录
cd ManagerApi

# 创建虚拟环境（如果使用）
python -m venv venv

# 激活虚拟环境
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 安装依赖
pip install -r requirements.txt  # 如果存在requirements.txt文件

# 运行数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

## 项目结构

```
StudenManager/
├── ManagerApi/           # 后端Django项目
│   ├── ManagerApi/       # 项目配置目录
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py         # Django管理脚本
├── manager-vue/          # 前端Vue项目
│   ├── public/           # 静态资源
│   │   ├── staticImg/    # 图片资源
│   │   └── staticVoid/   # 视频资源
│   ├── src/              # 源代码
│   │   ├── assets/       # 项目资源
│   │   ├── components/   # Vue组件
│   │   │   └── Login.vue # 登录组件
│   │   ├── routers/      # 路由配置
│   │   │   └── index.js  # 路由入口
│   │   ├── App.vue       # 根组件
│   │   ├── main.js       # 入口文件
│   │   └── settings.js   # 配置文件
│   └── package.json      # 项目依赖
├── environment.txt       # 环境配置文件
└── LICENSE               # 许可证文件
```

## API文档
*待补充*

## 注意事项
1. 开发环境配置需要确保Node.js和Python版本符合要求
2. 前端默认连接到后端地址 `http://127.0.0.1:8000`
3. 首次使用需要初始化数据库并创建管理员账号
4. 生产环境部署前需要修改相应的配置参数

## 待开发功能
1. 完善用户权限管理系统
2. 实现数据统计和图表展示
3. 添加宿舍评分和反馈功能
4. 集成消息推送系统
5. 优化移动端适配

---

*注：本项目为大学本科毕业设计作品，后续将持续完善。*