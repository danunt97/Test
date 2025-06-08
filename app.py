import os
import time

import requests
from flask import Flask, render_template, redirect, url_for, jsonify

app = Flask(__name__)

CAMERA_URL = os.environ.get('SONY_CAMERA_URL', 'http://192.168.122.1:10000/sony/camera')
IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'static')

def list_images():
    """Return a list of image filenames in the static directory."""
    if not os.path.isdir(IMAGE_DIR):
        return []
    return sorted(
        [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
        reverse=True,
    )


def capture_image():
    """Capture an image from the camera and return the stored filename."""
    payload = {
        "method": "actTakePicture",
        "params": [],
        "id": 1,
        "version": "1.0",
    }
    resp = requests.post(CAMERA_URL, json=payload, timeout=5)
    resp.raise_for_status()
    result = resp.json()
    if "result" in result:
        image_url = result["result"][0]
        img_data = requests.get(image_url, timeout=5).content
        filename = f"photo_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(img_data)
        return filename
    return None

@app.route('/')
def index():
    images = list_images()
    return render_template('index.html', images=images)

@app.route('/capture', methods=['POST'])
def capture():
    try:
        filename = capture_image()
        if filename:
            return redirect(url_for('show_image', filename=filename))
    except Exception as e:
        print('Error capturing image:', e)
    return redirect(url_for('index'))


@app.route('/api/capture', methods=['POST'])
def api_capture():
    """Capture an image and return JSON metadata."""
    try:
        filename = capture_image()
        if filename:
            return jsonify(success=True, filename=filename)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
    return jsonify(success=False), 500

@app.route('/image/<filename>')
def show_image(filename):
    return render_template('image.html', filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
