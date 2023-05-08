import pyaudio
import wave
from flask import Flask, Response

app = Flask(__name__)

def gen_audio_frames():
    # Set up audio capture
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    while True:
        # Read audio data from the audio stream
        audio_data = stream.read(1024)

        # Yield the audio as an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: audio/wav\r\n\r\n' + audio_data + b'\r\n')

@app.route('/audio')
def audio_feed():
    return Response(gen_audio_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
