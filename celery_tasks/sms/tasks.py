# 任务
from celery_tasks.sms.tencent_sms import sms
from celery_tasks.sms import constants
from celery_tasks.main import celery_app


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    异步发送短信

    :param mobile: 手机号

    :param sms_code: 验证码

    """
    sms.send(mobile, [sms_code, str(constants.SMS_CODE_REDIS_EXPIRES // 60)])
