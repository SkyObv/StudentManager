import socket
import time
import json
from machine import Pin 

"""socket服务"""
class Server:
    socket_class = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
    ip = None
    port = 8080
    
    def __init__(self,ip):
        self.ip = ip
        self.socket_class.bind((self.ip,self.port))
        self.socket_class.listen(5)
        print(f"服务器已启动，连接地址{self.ip}:{self.port}")
        
        try :
            while True:
                conn, addr = self.socket_class.accept()                   # 等待连接
                GPIO_list ,value = self._parse_requests(conn,addr)        # 解析数据
                self._operation(GPIO_list,value)                          # 操作函数
                conn.close()                                              # 关闭客户端连接
        finally:
            self.socket_class.close()                                     # 关闭服务
    
    """
    解析客户端请求
        conn 请求数据
        addr 客户端信息
    """
    def _parse_requests(self,conn,addr):
        print(f"客户端信息:{addr}")
        data = conn.recv(1024)
        print(data.decode())
        data = json.loads(data.decode())
        GPIO_list = data["GPIO"]                                          # GIPO控制列表
        value = data["value"]
        return GPIO_list,value

    """
    针脚控制
        GPIO_list 需要控制的引脚
        value     控制指令
    """
    def _operation(self,GPIO_list,value):
        for gpio in GPIO_list:
            if gpio is not None:
                pin = Pin(gpio, Pin.OUT)
                pin.value(value)
                if gpio == 16:
                    time.sleep(10)
                    pin.value(0)