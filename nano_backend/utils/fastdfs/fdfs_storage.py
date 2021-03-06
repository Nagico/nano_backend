import io
import logging
import os

from PIL import Image
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import get_tracker_conf, Fdfs_client

logger = logging.getLogger('fastdfs')


@deconstructible
class FastDFSStorage(Storage):
    def __init__(self, base_url=None, client_conf=None):
        """
        初始化
        :param base_url: 用于构造图片完整路径使用，图片服务器的域名
        :param client_conf: FastDFS客户端配置文件的路径
        """
        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.tracker_conf = get_tracker_conf(client_conf)
        # 判断是否有环境变量，如果有，则使用环境变量的值
        self.tracker_conf['host_tuple'] = (os.environ.get('FASTDFS_TRACKER_HOST', self.tracker_conf['host_tuple'][0]),)
        pass

    def _open(self, name, mode='rb'):
        """
        用不到打开文件，所以省略
        """
        pass

    def content_handler(self, name, content):
        """
        处理传入数据
        :param name: 文件名
        :param content: 文件内容
        :return:
        """
        return name, content

    def _save(self, name, content):
        """
        在FastDFS中保存文件
        :param name: 传入的文件名
        :param content: 文件内容
        :return: 保存到数据库中的FastDFS的文件名
        """
        client = Fdfs_client(self.tracker_conf)
        ext_name = None
        if '.' in name:
            ext_name = name.rsplit('.', 1)[1]
        name, content = self.content_handler(name, content)
        ret = client.upload_by_buffer(content.read(), file_ext_name=ext_name)
        if ret.get("Status") != "Upload successed.":
            raise Exception("upload file failed")
        file_name = ret.get("Remote file_id")
        logger.info(f'upload file success: {file_name}, info: {ret}')
        return file_name.decode()

    def delete(self, remote_file_id):
        client = Fdfs_client(self.tracker_conf)
        try:
            ret_delete = client.delete_file(str.encode(remote_file_id))
            logger.info(f'delete file success: {remote_file_id}')
            return ret_delete

        except Exception as e:
            logger.warning(f'delete file failed: {remote_file_id}, err: {e}')
            return None

    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名
        :return: 完整的URL
        """
        return self.base_url + name

    def exists(self, name):
        """
        判断文件是否存在，FastDFS可以自行解决文件的重名问题
        所以此处返回False，告诉Django上传的都是新文件
        :param name:  文件名
        :return: False
        """
        return False


@deconstructible
class FastDFSAvatarStorage(FastDFSStorage):
    def content_handler(self, name, content):
        """
        重写文件处理，压缩图片
        :param name:
        :param content:
        :return:
        """
        image = Image.open(content.file)

        # 标准化图片宽度
        if hasattr(settings, 'AVATAR_BASE_WIDTH') and image.width > settings.AVATAR_BASE_WIDTH:
            base_width = settings.AVATAR_BASE_WIDTH
            w_percent = base_width / float(image.size[0])
            h_size = int(float(image.size[1]) * float(w_percent))
            image = image.resize((base_width, h_size), Image.ANTIALIAS)

        # 转换格式
        new_image = io.BytesIO()
        image = image.convert('RGB')
        image.save(new_image, format='JPEG')
        new_image.seek(0)  # 返回游标到开始位置，因为后面要用到它的内容
        content.file = new_image
        content.content_type = 'image/jpeg'

        name = name.rsplit('.', 1)[0] + '.jpg'

        return name, content
