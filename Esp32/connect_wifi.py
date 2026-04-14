import network
import gc
import time
import settings


"""
wifi 连接
    
"""
class Connect_WiFI:
    wlan = None                                            # wlan 对象
    wifis = []                                             # 附近wifi列表
    select_wifi = None                                     # 选择的wifi
    timeout = 15                                           # 连接超时时间
    ip = None                                              # 连接成功后的ip地址
    
    def __init__(self):
        gc.collect()                                       # 手动触发垃圾回收
        print("空闲内存:", gc.mem_free(), "字节")           # 显示当前空闲内存
        self.wlan = network.WLAN(network.STA_IF)           # 创建wlan对象
        self.wlan.active(True)                             # 开启wifi
        
        # 开始循环连接wifi，直到连接成功
        while True:
            # 如果已经连上了，直接退出循环
            if self.wlan.isconnected():
                self.ip = self.wlan.ifconfig()[0]
                break
            try:
                self.scanning_wifi()
                self.connect()
            except:
                print("连接失败，重新连接！")
            finally:
                time.sleep(1)
            
    
    """扫描附近wifi"""
    def scanning_wifi(self):
        print(f"开始扫描附近的WiFi...")
        count = 0                                          # 计数器
        self.wifis = self.wlan.scan()
        for i in self.wifis:
            wifi_name = i[0].decode('utf-8')
            signal = i[3]
            print(f"=======第{count}个=====")
            print(f"名称：{wifi_name}")
            print(f"信号：{signal}")
            count += 1
        self.select_wifi = int(input("请选择wifi序号："))
    
    """连接wifi"""
    def connect(self):
        wifi_name = self.wifis[self.select_wifi][0].decode('utf-8')
        print(f"选择的wifi名称是：{wifi_name}")
        password = str(input("请输入wifi密码："))
        self.wlan.connect(wifi_name,password)
        start_time = time.time()
        
        while not self.wlan.isconnected():
            if time.time() - start_time > self.timeout:
                print("连接超时")
                return
            print("连接中...")
            time.sleep(2)
        self.ip = self.wlan.ifconfig()[0]
        print(f"   IP 地址: {self.wlan.ifconfig()[0]}")
        print(f"   子网掩码: {self.wlan.ifconfig()[1]}")
        print(f"   网关:     {self.wlan.ifconfig()[2]}")
        print(f"   DNS:      {self.wlan.ifconfig()[3]}")

# 根据配置文件自动链接wifi
class AutoConnect_Wifi:
    ip = None                                              # 连接成功后的ip地址
    wlan = None                                            # wlan 对象
    timeout = 15                                           # 连接超时时间
    
    def __init__(self):
        gc.collect()                                       # 手动触发垃圾回收
        print("空闲内存:", gc.mem_free(), "字节")           # 显示当前空闲内存
        self.wlan = network.WLAN(network.STA_IF)           # 创建wlan对象
        self.wlan.active(True)                             # 开启wifi
        self.connect()                                     # 开始连接wifi
    
    """连接wifi"""
    def connect(self):
        wifi_name = settings.WIFINAME
        password = settings.WIFIPASSWORD
        print(f"开始连接wifi名称是：{wifi_name}")
        
        self.wlan.disconnect()
        time.sleep(1)
        self.wlan.active(False)
        time.sleep(1)
        self.wlan.active(True)
        time.sleep(2)                                       # 等WiFi模块初始化完成
        
        self.wlan.connect(wifi_name,password)
        
        start_time = time.time()
        while not self.wlan.isconnected():
            if time.time() - start_time > self.timeout:
                print("连接超时")
                return
            print("连接中...")
            time.sleep(2)

        self.ip = self.wlan.ifconfig()[0]
        print(f"   IP 地址: {self.wlan.ifconfig()[0]}")
        print(f"   子网掩码: {self.wlan.ifconfig()[1]}")
        print(f"   网关:     {self.wlan.ifconfig()[2]}")
        print(f"   DNS:      {self.wlan.ifconfig()[3]}")
    
    

if __name__ == "__main__":
    connect = Connect_WiFI()