# 学生宿舍管理控制系统

---

## 项目结构

```
students-manager/
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
│   │   ├── users/               # 用户管理应用
│   │   │   ├── __init__.py
│   │   │   ├── admin.py         # 后台管理配置
│   │   │   ├── apps.py          # 应用配置
│   │   │   ├── filters.py       # 过滤功能
│   │   │   ├── models.py        # 数据模型
│   │   │   ├── serializer.py    # 数据序列化器
│   │   │   ├── tests.py         # 测试文件
│   │   │   ├── urls.py          # 应用URL配置
│   │   │   └── views.py         # 视图函数
│   │   ├── teacher/             # 教师管理应用
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── filters.py
│   │   │   ├── models.py
│   │   │   ├── permissions.py
│   │   │   ├── serializer.py
│   │   │   ├── tests.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   ├── mycelery/                # Celery异步任务
│   │   ├── manager_task/        # 管理任务
│   │   │   └── create_student.py
│   │   ├── text/                # 测试任务
│   │   │   ├── __init__.py
│   │   │   └── excel_analysis.py
│   │   ├── __init__.py
│   │   ├── config.py            # Celery配置
│   │   └── main.py              # Celery主文件
│   ├── uploads/                 # 上传文件目录
│   ├── logs/                    # 日志目录
│   │   └── sm.log               # 系统日志文件
│   └── manage.py                # Django管理脚本
├── manager-vue/                  # 前端Vue项目
│   ├── public/                   # 静态资源
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── staticVoid/          # 视频资源
│   ├── src/                     # 源代码
│   │   ├── assets/              # 项目资源
│   │   │   └── logo.png
│   │   ├── components/          # Vue组件
│   │   │   ├── Admin.vue        # 管理员主组件
│   │   │   ├── AdminComp/       # 管理员子组件
│   │   │   │   ├── CardIDManage.vue   # 卡片管理组件
│   │   │   │   ├── FloorManage.vue    # 楼层管理组件
│   │   │   │   ├── HanderComp.vue     # 处理组件
│   │   │   │   ├── HostelLog.vue      # 宿舍日志组件
│   │   │   │   ├── HostelManage.vue   # 宿舍管理组件
│   │   │   │   └── TeacherManage.vue  # 教师管理组件
│   │   │   ├── Login.vue        # 登录组件
│   │   │   ├── Students.vue     # 学生端组件
│   │   │   ├── Teachers.vue     # 教师端组件
│   │   │   ├── TeacherComp/     # 教师子组件
│   │   │   │   ├── ApplyHostel.vue        # 申请宿舍组件
│   │   │   │   ├── ApplyHostelLogs.vue    # 申请记录组件
│   │   │   │   ├── CardIDManage.vue       # 卡片管理组件
│   │   │   │   ├── HeaderComp.vue         # 头部组件
│   │   │   │   ├── MyHostels.vue          # 我的宿舍组件
│   │   │   │   └── Mystudents.vue         # 我的学生组件
│   │   │   └── publicComp/      # 公共组件
│   │   │       ├── ApplyHostelCard.vue    # 申请宿舍卡片
│   │   │       ├── ApplyInfoCard.vue      # 申请信息卡片
│   │   │       ├── HostelInfoCard.vue     # 宿舍信息卡片
│   │   │       ├── StudentSelect.vue      # 学生选择组件
│   │   │       ├── StudentsTable.vue      # 学生表格组件
│   │   │       └── TripsCard.vue          # 行程卡片组件
│   │   ├── routers/             # 路由配置
│   │   │   └── index.js
│   │   ├── App.vue              # 根组件
│   │   ├── main.js              # 入口文件
│   │   └── settings.js          # 配置文件
│   ├── README.md
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   └── vue.config.js
├── Esp32/                        # ESP32相关代码
│   ├── connect_wifi.py
│   ├── main.py
│   ├── server.py
│   ├── settings.py
│   └── text.py
├── 测试导入文件数据/              # 测试数据目录
│   └── 测试数据.xlsx
├── .gitignore
├── LICENSE
├── README.md                    # 项目说明文档
├── environment.txt              # Python依赖文件
└── 学生宿舍管理系统数据库设计.json  # 数据库设计文件
```

## 简介
本项目是一个“学生宿舍管理控制系统”，包含后端管理接口（Django + Django REST framework）与前端管理页面（Vue）。系统以 JWT 认证区分用户角色，并提供楼层/宿舍管理、学生导入（Celery 异步）、宿舍申请审批、以及门禁卡管理等功能。

## 技术栈
- **后端**：Django 5 + DRF（Django REST framework）+ `djangorestframework_simplejwt`
- **数据库**：MySQL（默认配置见 `ManagerApi/ManagerApi/settings/dev.py`）
- **异步任务**：Celery + Redis
- **前端**：Vue 2.6 + Element UI + Axios

## 功能概览（按角色）
1. **管理者**（`user_type=admin`，前端路由 `AdminComp`）
   - 楼层管理：创建/删除楼层（楼层与宿舍为软删除）
   - 宿舍管理：创建/删除宿舍（宿舍为软删除）
   - 学生/教师账号管理：创建教师、禁用/恢复/彻底删除教师、给宿舍指定管理员
   - 宿舍申请记录查看：获取待审核申请（`apply_state=待审核`）
   - 卡片管理：管理门禁卡相关功能

2. **教师**（`user_type=teacher`，前端路由 `TeacherComp`）
   - 学生导入：上传 `.xlsx`，由 Celery 异步生成学生账号
   - 宿舍申请：获取可申请宿舍、提交申请、查看申请记录、更新申请状态
   - 我的宿舍管理：获取自己管理的宿舍，并对宿舍内学生进行增删
   - 门禁卡管理：查询与更新门禁卡状态（`TripsLog`）
   - 学生管理：查看和管理自己名下的学生

3. **学生**（`user_type=student`，前端路由 `StudentComp`）
   - 当前前端 `Students.vue` 仅为占位页面；后端仍支持登录与鉴权（`user_type=student`）。

## 快速开始（建议按顺序）
### 1）准备后端环境
1. 安装依赖：
```bash
pip install -r environment.txt
```
2. 配置数据库与基础设置（必做）：
   - 编辑 `ManagerApi/ManagerApi/settings/dev.py`
     - 修改 `DATABASES` 的 MySQL 账号密码与数据库名
     - 修改 `SECRET_KEY`
     - 确保 `MEDIA_ROOT` 指向的 `uploads/` 目录存在（用于接收导入文件）
3. 执行数据库迁移：
```bash
python ManagerApi/manage.py makemigrations
python ManagerApi/manage.py migrate
```
4. 启动后端服务：
```bash
python ManagerApi/manage.py runserver 127.0.0.1:8000
```

### 2）启动 Redis 与 Celery Worker
1. 启动 Redis（默认使用 `127.0.0.1:6379`）
2. 在项目目录 `ManagerApi/` 下执行 worker：
```bash
cd ManagerApi
celery -A mycelery.main worker -l info
```

说明：项目里 Celery 使用不同 Redis 数据库编号：broker 使用 `db=15`，结果使用 `db=14`（见 `mycelery/config.py`）。

### 3）启动前端
```bash
cd manager-vue
npm install
npm run serve
```

前端后端地址在 `manager-vue/src/settings.js` 中配置（默认 `http://127.0.0.1:8000`）。

## JWT 鉴权与请求头
1. 登录接口：`POST /users/login/`
   - 请求体（JSON）必须包含：`username`、`password`、`user_type`（`student | teacher | admin`）
2. 返回包含：`access`（访问令牌）、`refresh`（刷新令牌）、`user_type`、`name`
3. 访问接口时，前端使用的请求头为：
   - `Authorization: Hander <access_token>`

> 注：项目在 `SIMPLE_JWT` 中设置了 `AUTH_HEADER_TYPES=('Hander',)`，因此不是标准的 `Bearer`。

4. 刷新令牌接口：`POST /users/refresh/`
   - 由 `TokenRefreshView` 提供（一般请求体包含 `refresh` 字段）。

## 关键后端接口（API 路由清单）
### `users/`（登录 + 管理者/基础数据）
- `POST /users/login/`：JWT 登录（JSON：`username/password/user_type`）
- `POST /users/refresh/`：刷新令牌
- `GET /users/floors/`：获取所有楼层
- `GET /users/hostel/<floor_id>/`：获取某楼层的宿舍列表
- `GET /users/students/`：获取所有学生
- `GET /users/teachers/`：获取所有老师
- `POST /users/create/floor/`：创建楼层（JSON：`floor_name`）
- `DELETE /users/delete/<pk>/floor`：删除楼层（软删除）
- `POST /users/create/hostel/`：创建宿舍（至少提供：`floor`、`hostel_number`）
- `DELETE /users/delete/<pk>/hostel/`：删除宿舍（软删除并清空宿舍内学生）
- `DELETE /users/delete/fromhostel/student/?username=<username>`：从宿舍中删除学生
- `POST /users/add/fromhostel/student/`：为学生分配宿舍（JSON：`username`、`hostel_id`）
- `POST /users/craete/teacher/`：创建教师账号（路径拼写为 `craete`；JSON 字段同创建用户序列化器）
- `DELETE /users/delete/<pk>/teacher`：禁用老师账号
- `POST /users/restore/<pk>/teacher`：恢复老师账号
- `DELETE /users/delete/permanently/<pk>/teacher`：彻底删除老师账号
- `POST /users/add/hostel/manager/`：给宿舍指定管理员（JSON：`username`、`hostel_id`）
- `DELETE /users/add/hostel/manager/?pk=<hostel_id>`：删除宿舍管理员
- `GET /users/getall/hostellogs`：获取所有待审核宿舍申请记录

### `teacher/`（教师业务）
- `GET /teacher/get/allStudents/`：获取教师名下学生列表
- `POST /teacher/import/students/`：导入学生（`multipart/form-data`，文件字段名为 `file`，格式为 `.xlsx`）
- `GET /teacher/get/status/?task_id=<task_id>`：查询导入任务状态/结果
- `GET /teacher/get/hostel/`：获取可申请宿舍列表
- `POST /teacher/apply/hostel/`：申请宿舍（JSON：`hostel` = 宿舍 ID）
- `GET /teacher/get/applyRecord/`：获取我的申请记录
- `PUT /teacher/apply/upadte/<pk>/`：更新申请状态（URL 拼写为 `upadte`；JSON：`apply_state`）
- `DELETE /teacher/apply/delete/<pk>/`：删除申请记录
- `GET /teacher/myhostel/allget/`：获取我的宿舍及宿舍内学生信息
- `DELETE /teacher/myhostel/delete/studentTohostel/?pk=<student_id>`：从宿舍中移除学生
- `POST /teacher/myhostel/add/studentTohostel/`：将学生加入宿舍（JSON：`hostel_id`、`student_ids`）
- `GET /teacher/trips/get/all`：查询门禁卡记录（`TripsLog`）
- `PUT /teacher/trips/update/?id=<trips_log_id>`：更新门禁卡状态
- `POST /teacher/text/celery/`：Celery 测试接口

## 学生导入（Excel 模板要求）
导入学生通过 Celery 异步处理，Excel 需要包含这些中文列名（代码中会做字段映射）：
- `学号` -> `username`
- `密码` -> `password`
- `姓` -> `last_name`
- `名` -> `first_name`
- `性别` -> `gender`
- `指导老师` -> `teacher_id`（对应教师账号的 `username`）

## 业务规则补充
- **宿舍容量**：`Hostel.capacity` 默认是 6；添加学生时会限制超出容量的情况。
- **删除策略**：楼层/宿舍存在软删除字段（`is_deleted`），删除后部分接口支持恢复逻辑。
- **JWT 认证**：使用自定义的 `Hander` 认证头部，而非标准的 `Bearer`。

## 前端技术栈
- Vue 2.6.14
- Vue Router 3.6.5
- Element UI 2.15.14
- Axios 1.13.2

## 后端技术栈
- Django 5.2.8
- Django REST framework 3.16.1
- Django REST framework Simple JWT 5.5.1
- Celery 5.6.0
- Redis 6.4.0
- MySQL 5.7+
- Pandas 2.3.3（用于Excel处理）

## 注意事项
1. 确保 Redis 服务正常运行，否则 Celery 任务无法执行
2. 数据库配置必须正确，否则后端服务无法启动
3. 前端与后端的地址配置必须一致，否则无法正常通信
4. 学生导入功能需要确保 Excel 文件格式正确，否则可能导致导入失败
5. 本项目为开发环境配置，生产环境需要进行相应的安全配置

## 许可证
本项目采用 MIT 许可证，详情见 LICENSE 文件。