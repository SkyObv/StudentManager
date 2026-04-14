from connect_wifi import Connect_WiFI,AutoConnect_Wifi
from server import Server

# 终端连接wifi
# conn = Connect_WiFI()

# 根据配置自动连接wifi
conn = AutoConnect_Wifi()
print(f"当前ip : {conn.ip}")

# 服务路由

# 开启服务
server = Server(ip=conn.ip)