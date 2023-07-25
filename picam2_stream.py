import picamera
import picamera.array


# Initialize the PiCamera object
camera = picamera.PiCamera()

# Set the camera resolution and framerate
camera.resolution = (640, 480)
camera.framerate = 24

# Start the RTSP server
rtsp_url = 'rtsp://0.0.0.0:8554/mystream'
server = picamera.PiCameraServer(rtsp_url, port=8554)
server.start()

# Start the camera capture and streaming
with picamera.array.PiRGBArray(camera, size=camera.resolution) as output:
    for frame in camera.capture_continuous(output, format='bgr', use_video_port=True):
        # Get the latest frame from the camera
        img = frame.array

        # Send the frame to the RTSP server
        server.send_video_frame(img)

        # Clear the output buffer for the next frame
        output.truncate(0)

        # Display the frame locally (optional)
        print(f"THere is a frame ")

# Stop the RTSP server and release resources
server.stop()
