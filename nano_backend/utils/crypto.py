# rsa 加解密
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from django_redis import get_redis_connection


class Crypto:
    def __init__(self, pub_key='keys/pub.key', pri_key='keys/pri.key'):
        try:
            redis_conn = get_redis_connection('default')  # 获取redis连接
            pub_key_str = redis_conn.get(f'pub_key')  # 尝试从redis中获取公钥
            pri_key_str = redis_conn.get(f'pri_key')  # 尝试从redis中获取私钥

            if not pub_key_str and not pri_key_str:  # 如果redis中没有公钥和私钥，则从文件中读取
                pl = redis_conn.pipeline()  # 创建管道
                with open(pri_key, 'rb') as f:  # 读取私钥
                    pri_key_str = f.read()  # 文件读入私钥
                    pl.set(f'pri_key', pri_key_str)  # 将私钥写入redis
                with open(pub_key, 'rb') as f:  # 读取公钥
                    pub_key_str = f.read()  # 文件读入公钥
                    pl.set(f'pub_key', pub_key_str)  # 将公钥写入redis
                pl.execute()  # 执行管道
        except:  # 非 Django 环境下运行
            with open(pri_key, 'rb') as f:  # 读取私钥
                pri_key_str = f.read()  # 文件读入私钥
            with open(pub_key, 'rb') as f:  # 读取公钥
                pub_key_str = f.read()  # 文件读入公钥

        self.pri_cipher = PKCS1_cipher.new(RSA.importKey(pri_key_str))  # 创建私钥加密对象
        self.pub_cipher = PKCS1_cipher.new(RSA.importKey(pub_key_str))  # 创建公钥加密对象

    def encrypt(self, message):
        """
        加密
        """
        rsa_text = base64.b64encode(self.pub_cipher.encrypt(bytes(message.encode('utf8'))))
        return rsa_text.decode('utf8')

    def decrypt(self, rsa_text):
        """
        解密
        """
        back_text = self.pri_cipher.decrypt(base64.b64decode(rsa_text), 0)
        return back_text.decode('utf-8')


if __name__ == '__main__':
    c = Crypto('../../keys/pub.key', '../../keys/pri.key')
    text = '123456789'
    print(c.encrypt(text))
    print(c.encrypt(text))
    print(c.decrypt(c.encrypt(text)))
