import socket

# Create socket for server
cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set resolution
# Some kind of reset required
payload = bytes.fromhex('534554434d44 00140000 90000100 00')
cmd_sock.sendto(payload, ('192.168.10.123', 50000))
cmd_sock.recvfrom(50)

# Lol, does not support 1080. Scaling is done somewhere.
# 1280x720: 0005 D002
# 960x720: C003 D002
# 640x480: 8002 E001
payload = bytes.fromhex('534554434d44 00000000 08000500 c003 d002 14')
cmd_sock.sendto(payload, ('192.168.10.123', 50000))
cmd_sock.recvfrom(50)

# Ask for supported resolutions
# 524554434d4401000000 09000010 00 03 0005 d002 14 c003 d002 14 8002 e001
payload = bytes.fromhex('534554434d44 01000000 09000000')
cmd_sock.sendto(payload, ('192.168.10.123', 50000))

print(cmd_sock.recvfrom(50)[0].hex())
