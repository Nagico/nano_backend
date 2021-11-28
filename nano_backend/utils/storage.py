import io
import os
import time
import random
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class AvatarStorage(FileSystemStorage):
    """
    头像存储
    """
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(AvatarStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        """
        重写 _save方法
        """
        image = Image.open(content.file)

        # 标准化图片宽度
        if settings.AVATAR_BASE_WIDTH:
            base_width = settings.AVATAR_BASE_WIDTH
            w_percent = base_width / float(image.size[0])
            h_size = int(float(image.size[1]) * float(w_percent))
            image = image.resize((base_width, h_size), Image.ANTIALIAS)

        # 转换格式
        new_image = io.BytesIO()
        image = image.convert('RGB')
        image.save(new_image, format='JPEG')
        content.file = new_image
        content.content_type = 'image/jpeg'

        # 随机化文件名
        ext = '.jpg'  # 文件扩展名
        d = os.path.dirname(name)  # 文件目录

        fn = time.strftime('%Y%m%d%H%M%S')  # 定义文件名，年月日时分秒随机数
        fn = fn + '_%d' % random.randint(0, 100)

        name = os.path.join(d, fn + ext)  # 重写合成文件名

        return super(AvatarStorage, self)._save(name, content)
