import socket
import datetime
import struct

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind(('localhost', 7060))

tcp_sock.listen()

print("Waiting for connection")
conn, addr = tcp_sock.accept()
print("Let's go")

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

payload = bytes.fromhex('999901000000000000000000000000000000000000000000')

udp_sock.sendto(payload, ('192.168.10.123', 8030))
next_send = datetime.datetime.now() + datetime.timedelta(0,1)

def encode_index(sequence, img_size):
    r0 = sequence ^ img_size
    r2 = 1 & (img_size ^ 0xff)
    r0 += img_size + r2
    r0 ^= img_size
    return r0 % img_size

sent = 9999999

while True:
    if datetime.datetime.now() > next_send:
        udp_sock.sendto(payload, ('192.168.10.123', 8030))
        next_send = datetime.datetime.now() + datetime.timedelta(0,1)

    data, address = udp_sock.recvfrom(0xc4f)
    if data[2] == 3:
        mjpeg_data = bytearray(data[0x33:])

        (frame, ) = struct.unpack('<H', data[0x27:0x29])
        (chunk, ) = struct.unpack('<H', data[0x21:0x23])
        (frame_size, ) = struct.unpack('<H', data[0x1D:0x1F])
        chunk_size = len(mjpeg_data)
        if chunk == 1:
            sent = 0
        
        flipped_index = encode_index(frame, frame_size)

        if flipped_index > sent and flipped_index < sent + chunk_size:
            local_flip_index = flipped_index - sent
            mjpeg_data[local_flip_index] ^= 0xff

        conn.sendall(mjpeg_data)
        sent += chunk_size

# close the socket
udp_sock.close()
