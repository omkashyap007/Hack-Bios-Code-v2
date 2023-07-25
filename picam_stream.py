import socket
import io
import picamera

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
PORT = 8554

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(1)

print(f'Starting RTSP server on port {PORT}')

with picamera.PiCamera() as camera:
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = FRAMERATE
    count = 0
    while True:
        client_socket, _ = server_socket.accept()
        count+=1
        print(f'New client {count} connected')

        client_socket.send(b'RTSP/1.0 200 OK\r\n\r\n')

        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            data = (b'\xff'*4) + stream.getvalue() + (b'\x00'*4)
#             print(data)
            client_socket.send(data)
            stream.seek(0)
            stream.truncate()

            try:
                _ = client_socket.recv(1, socket.MSG_DONTWAIT)
            except Exception as e :
                print("The error is : {e}")
            else:
                break

        client_socket.close()
