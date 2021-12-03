from celery import Celery

# 创建celery应用
celery_app = Celery('nano_backend')

# 加载配置文件
celery_app.config_from_object('celery_tasks.config')

# 注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])

# celery -A celery_tasks.main worker -l info -P eventlet
