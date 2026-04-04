from connect_wifi import Connect_WiFI
from server import Server

# 连接wifi
conn = Connect_WiFI()
print(f"当前ip : {conn.ip}")

# 服务路由

# 开启服务
server = Server(ip=conn.ip)