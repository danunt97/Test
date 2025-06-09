import ctypes
import os

_lib = None


def _load_library():
    global _lib
    if _lib is not None:
        return
    lib_path = os.environ.get('SONY_SDK_PATH')
    if not lib_path or not os.path.exists(lib_path):
        raise RuntimeError('Sony SDK library not found. Set SONY_SDK_PATH.')
    _lib = ctypes.cdll.LoadLibrary(lib_path)


def capture_image(filepath: str):
    """Capture an image using the Sony Camera Remote SDK."""
    _load_library()
    # This example assumes the SDK exposes a function named CaptureImage that
    # takes a file path as a C string and returns 0 on success.
    c_path = ctypes.c_char_p(filepath.encode('utf-8'))
    result = _lib.CaptureImage(c_path)
    if result != 0:
        raise RuntimeError('CaptureImage failed with code %s' % result)


def get_liveview_frame() -> bytes:
    """Return a single JPEG frame from the camera's live view."""
    _load_library()
    # This assumes the SDK exposes GetLiveViewFrame(buffer, size) returning
    # the number of bytes written into the buffer. Adjust as needed for the
    # real SDK. These calls are placeholders for demonstration only.
    buf_size = 2 * 1024 * 1024
    buf = (ctypes.c_ubyte * buf_size)()
    written = _lib.GetLiveViewFrame(buf, buf_size)
    if written <= 0:
        raise RuntimeError('GetLiveViewFrame failed')
    return bytes(buf[:written])

