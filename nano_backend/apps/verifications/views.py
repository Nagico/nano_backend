import logging
from random import randint

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework import status

from . import constants
from celery_tasks.sms.tasks import send_sms_code

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    """
    短信验证码验证
    """

    permission_classes = [AllowAny]  # 允许任何人

    def get(self, request, mobile):
        """
        获取短信验证码
        :param request:
        :param mobile:
        :return:
        """
        # 创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 检查标记
        send_flag = redis_conn.get(f'sms_flag_{mobile}')

        if send_flag:  # 取到标记
            logger.info(f'短信验证码发送过于频繁，{mobile}')
            return Response({'message': '发送短信过于频繁'}, status=status.HTTP_400_BAD_REQUEST)

        # 生成验证码
        sms_code = '%06d' % randint(0, 999999)
        logger.info(f'{mobile} 短信验证码为：{sms_code}')

        # 创建 redis 管道(管道可以一次执行多个命令，提高效率)
        pl = redis_conn.pipeline()

        # 存储验证码
        pl.setex(f'sms_{mobile}', constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex(f'sms_flag_{mobile}', constants.SEND_SMS_CODE_INTERVAL, 1)  # 存入60秒的标记

        pl.execute()

        # celery 异步发送短信
        send_sms_code.delay(mobile, sms_code)

        # 响应
        return Response({'message': 'OK'})
