# Sony Photo Booth

This example provides a simple Flask-based photo booth that communicates
with Sony cameras using the official **Sony Camera Remote SDK** over USB. It
offers a live view preview in the browser, a short countdown before each
capture and a white flash effect when the shutter is triggered. Captured
photos are stored locally so they can be viewed in a gallery.

## Requirements

- Python 3
- `flask` package
- Sony Camera Remote SDK for your platform

Download the SDK from Sony and note the path to the library file (e.g.
`libSonyCameraSDK.so` on Linux or `SonyCameraSDK.dll` on Windows). The
application looks for this path via the `SONY_SDK_PATH` environment variable.

## Usage

1. Install dependencies (preferably in a virtual environment):

```bash
pip install flask
```

2. Connect your Sony camera via USB and install the Sony Camera Remote SDK.
   Set the environment variable `SONY_SDK_PATH` to the path of the library
   file provided by the SDK so the application can load it.

3. Run the application:

```bash
python app.py
```

4. Open a browser to `http://localhost:5000` and press **Take Picture** to
   capture an image. Captured images are stored in the `static` folder and
   displayed in a simple gallery on the main page. When JavaScript is enabled
   the page shows a live preview from the camera. Press the button to start a
   three‑second countdown; a brief white flash indicates the moment of capture
   and the new thumbnail appears automatically. Click any thumbnail to view the
   full image.
