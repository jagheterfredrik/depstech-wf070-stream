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

while True:
    if datetime.datetime.now() > next_send:
        udp_sock.sendto(payload, ('192.168.10.123', 8030))
        next_send = datetime.datetime.now() + datetime.timedelta(0,1)

    data, address = udp_sock.recvfrom(0xc4f)
    if data[2] == 3:
        mjpeg_data = bytearray(data[0x33:])

        (frame, ) = struct.unpack('<I', data[0x27:0x2B])
        (chunk, ) = struct.unpack('<H', data[0x21:0x23])
        (frame_size, ) = struct.unpack('<I', data[0x1D:0x21])
        chunk_size = len(mjpeg_data)
        
        flipped_index = encode_index(frame, frame_size)

        mjpeg_chunk_offset = (chunk - 1) * 0x56e
        if flipped_index > mjpeg_chunk_offset and flipped_index < mjpeg_chunk_offset + chunk_size:
            local_flip_index = flipped_index - mjpeg_chunk_offset
            mjpeg_data[local_flip_index] ^= 0xff

        conn.sendall(mjpeg_data)

# close the socket
udp_sock.close()
