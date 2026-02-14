import os
from celery import Celery
import django

# 设置djngo环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ManagerApi.settings.dev')
django.setup()                                                    # 创建django实例，使用ORM模型

# 创建Celery实例
app = Celery("student")                                           # 为Celery起一个项目名称
# 从Django的设置文件中加载Celery配置
app.config_from_object("mycelery.config")                         # 加载连接配置文件 config.py
# 自动发现任务
app.autodiscover_tasks([])                                        # 任务文件夹