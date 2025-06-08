# Sony Photo Booth

This example provides a simple Flask-based web application that can trigger
image capture on supported Sony cameras using the camera's Remote API.

## Requirements

- Python 3
- `flask` and `requests` packages
- Sony camera with Remote API support

## Usage

1. Install dependencies (preferably in a virtual environment):

```bash
pip install flask requests
```

2. Connect your Sony camera in remote control mode and ensure it is on the
   same network as this application. Obtain the camera's API URL (typically
   `http://<camera-ip>:10000/sony/camera`) and set it via the environment
   variable `SONY_CAMERA_URL` if different from the default.
   Images are stored in the `static` directory alongside the application.

3. Run the application:

```bash
python app.py
```

4. Open a browser to `http://localhost:5000` and press **Take Picture** to
   capture an image. Captured images are stored in the `static` folder and
   displayed in a simple gallery on the main page. When JavaScript is enabled
   the gallery updates automatically without reloading the page. Click any
   thumbnail to view the full image.
