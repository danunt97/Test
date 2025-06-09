import os
import time

from flask import Flask, render_template, redirect, url_for, jsonify, Response

import sony_sdk

app = Flask(__name__)

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
    """Capture an image via the Sony Camera Remote SDK and return the stored filename."""
    os.makedirs(IMAGE_DIR, exist_ok=True)
    filename = f"photo_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(IMAGE_DIR, filename)

    try:
        sony_sdk.capture_image(filepath)
        return filename
    except Exception:
        if os.path.exists(filepath):
            os.remove(filepath)
        raise

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


@app.route('/api/liveview')
def api_liveview():
    """Return a single JPEG frame from the camera's live view."""
    try:
        frame = sony_sdk.get_liveview_frame()
        return Response(frame, mimetype='image/jpeg')
    except Exception as e:
        print('Live view error:', e)
        return Response(status=500)

@app.route('/image/<filename>')
def show_image(filename):
    return render_template('image.html', filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
