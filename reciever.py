from gbvision import CameraData, Camera, AsyncCamera
from gbvision.models.cameras import UNKNOWN_CAMERA
import gbvision as gbv
import cv2
import platform


class SecretCamera(cv2.VideoCapture, Camera):
    """
    a basic usb connected camera which inherits from cv2 VideoCapture

    :param port: the usb port to which the camera is connected
    :param data: the camera data object that describes this camera
    """

    ARAZI = "http://132.64.143.185:5000/video_feed"
    DANIEL = "http://132.64.143.105:5000/video_feed"

    def __init__(self, address: str, data: CameraData = UNKNOWN_CAMERA):
        """
        initializes the camera

        """
        cv2.VideoCapture.__init__(self, address, cv2.CAP_FFMPEG)
        self._data = data.copy()
        self.bbox = None

    def is_opened(self) -> bool:
        return self.isOpened()

    @staticmethod
    def __is_on_linux() -> bool:
        return platform.system() == 'Linux'

    def manually_bound(self):
        frame = self._read()
        self.bbox = cv2.selectROI('feed', frame[1])

    def _read(self, image=None):
        return cv2.VideoCapture.read(self, image)

    def read(self, image=None):
        inp = self._read(image)
        return inp[0], gbv.crop(inp[1], *self.bbox) if self.bbox is not None else inp[1]

    def set_exposure(self, exposure) -> bool:
        return False

    def set_auto_exposure(self, auto) -> bool:
        return False

    def get_data(self):
        return self._data

    def get_width(self):
        return self.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_height(self):
        return self.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def _set_width(self, width):
        return self.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    def _set_height(self, height):
        return self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_fps(self):
        return self.get(cv2.CAP_PROP_FPS)

    def set_fps(self, fps):
        return self.set(cv2.CAP_PROP_FPS, fps)
