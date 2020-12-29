import cv2
import numpy as np
from reciever import SecretCamera

import gbvision as gbv

s = SecretCamera(SecretCamera.DANIEL)

# ColorThreshold([[176, 255], [198, 255], [155, 255]], 'RGB')

# ColorThreshold([[200, 255], [202, 255], [201, 255]], 'RGB') !!!WHITE ON BLACK!!!

stdv = np.array([50, 50, 50])
stdv = 30


class ImageProcessing:
    INTERPOLATION = cv2.INTER_CUBIC
    STDV = 50

    def __init__(self, camera):
        self.camera = camera
        self.camera_init()
        self.window = gbv.CameraWindow('feed', camera)
        self.window.open()
        self.pipeline = None
        self.bbox_bound = None
        self.bbox_pipeline = None
        self.current_original_frame = None
        self.current_cropped_frame = None
        self.current_piped_frame = None

    def setup(self):
        self.crop_init()
        self.init_pipeline()
        cv2.destroyAllWindows()

    def camera_init(self):
        self.camera.set_exposure(-5)
        self.camera.resize(.1, .1)

    def crop_init(self):
        frame = self.get_original_frame()
        self.bbox_bound = cv2.selectROI('feed', frame)

    def init_pipeline(self, *temp_args):
        # pipeline = gbv.ColorThreshold([[0, 100], [0, 255], [0, 255]], 'HSV')

        self.get_cropped_frame()
        bbox = cv2.selectROI('feed', self.current_cropped_frame)
        self.pipeline = gbv.median_threshold(self.current_cropped_frame, ImageProcessing.STDV, bbox, 'RGB')
        print(self.pipeline)
        # pipeline += gbv.ErodeAndDilate(2)
        return self.pipeline

    def get_original_frame(self):
        ok, self.current_original_frame = self.camera.read()
        return self.current_original_frame

    def get_cropped_frame(self):
        frame = gbv.crop(self.current_original_frame, *self.bbox_bound)
        self.current_cropped_frame = cv2.resize(frame, (800, 800), interpolation=ImageProcessing.INTERPOLATION)
        return self.current_cropped_frame

    def get_piped_frame(self):
        return self.pipeline(self.current_cropped_frame)

    def get_frame(self):
        self.get_original_frame()
        self.get_cropped_frame()
        return self.get_piped_frame()


def main():
    # camera = gbv.USBCamera(0)
    camera = gbv.USBCamera(r"C:\Users\t8854535\Desktop\sprint2\test_data\record.avi")
    imgp = ImageProcessing(camera)
    imgp.setup()

    original = gbv.FeedWindow(window_name='original')
    after_proc = gbv.FeedWindow(window_name='after threshold')

    original.open()
    after_proc.open()

    while True:
        after_frame = imgp.get_frame()
        original_frame = imgp.current_cropped_frame
        if not original.show_frame(original_frame):
            break
        if not after_proc.show_frame(after_frame):
            break


if __name__ == '__main__':
    main()
