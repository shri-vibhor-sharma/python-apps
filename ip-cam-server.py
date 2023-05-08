import cv2
from flask import Flask, Response

app = Flask(__name__)

def gen_frames(camera):
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()

        if not ret:
            break

        # Convert the frame to bytes
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

        # Yield the frame as an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/camera/<int:camera_id>')
def camera_feed(camera_id):
    # Set up camera connection
    cap = cv2.VideoCapture(camera_id)

    # Set camera resolution and FPS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    return Response(gen_frames(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    html = '<h1>Available Cameras:</h1><ul>'

    # Iterate over all camera devices and generate links to their feeds
    for camera_id in range(0, 10):
        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():
            continue

        html += f'<li><a href="/camera/{camera_id}">Camera {camera_id}</a></li>'

        cap.release()

    html += '</ul>'

    return html

if __name__ == '__main__':
    app.run(debug=True)
