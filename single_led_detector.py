import cv2
import numpy as np
from reciever import SecretCamera

import gbvision as gbv

s = SecretCamera(SecretCamera.ARAZI)

# ColorThreshold([[176, 255], [198, 255], [155, 255]], 'RGB')

# ColorThreshold([[200, 255], [202, 255], [201, 255]], 'RGB') !!!WHITE ON BLACK!!!


class ImageProcessing:
    INTERPOLATION = cv2.INTER_CUBIC
    STDV = 50
    WHITE = "WHITE"
    RED = "RED"

    def __init__(self, camera):
        self.camera = camera
        self.camera_init()
        self.window = gbv.CameraWindow('feed', camera)
        self.window.open()
        self.pipelines = {ImageProcessing.WHITE: None, ImageProcessing.RED: None}
        self.bbox_bound = None
        self.current_original_frame = None
        self.current_cropped_frame = None
        self.current_piped_frame = None

    def setup(self):
        self.next_frame()
        self.crop_init()
        self.init_pipeline(ImageProcessing.WHITE)
        self.init_pipeline(ImageProcessing.RED)
        cv2.destroyAllWindows()

    def camera_init(self):
        #self.camera.set_exposure(-5)
        #self.camera.resize(.1, .1)
        pass

    def crop_init(self):
        frame = self.get_original_frame()
        self.bbox_bound = cv2.selectROI('feed', frame)

    def init_pipeline(self, color):
        # pipeline = gbv.ColorThreshold([[0, 100], [0, 255], [0, 255]], 'HSV')

        self.get_cropped_frame()
        bbox = cv2.selectROI('feed', self.current_cropped_frame)
        self.pipelines[color] = gbv.median_threshold(self.current_cropped_frame, ImageProcessing.STDV, bbox, 'RGB')
        print(self.pipelines)
        self.pipelines[color] += gbv.ErodeAndDilate(20)
        return self.pipelines[color]

    def next_frame(self):
        ok, self.current_original_frame = self.camera.read()
        if not ok:
            raise NotImplementedError()

    def get_original_frame(self):
        return self.current_original_frame

    def get_cropped_frame(self):
        frame = gbv.crop(self.current_original_frame, *self.bbox_bound)
        self.current_cropped_frame = cv2.resize(frame, (1000, 1000), interpolation=ImageProcessing.INTERPOLATION)
        return self.current_cropped_frame

    def get_piped_frame(self, color):
        return self.pipelines[color](self.current_cropped_frame)

    def get_frame(self, color):
        self.get_original_frame()
        self.get_cropped_frame()
        return self.get_piped_frame(color)

def main():
    #camera = gbv.USBCamera(0)
    camera = gbv.USBCamera(r"C:\Users\t8854535\Desktop\sprint2\test_data\total_test.avi")
    #camera = s
    imgp = ImageProcessing(camera)
    imgp.setup()

    original = gbv.FeedWindow(window_name='original')
    white_filtered = gbv.FeedWindow(window_name='white')
    red_filtered = gbv.FeedWindow(window_name='red')

    original.open()
    white_filtered.open()
    red_filtered.open()

    while True:
        try:
            imgp.next_frame()
        except NotImplementedError:
            return
        white_frame = imgp.get_frame(ImageProcessing.WHITE)
        red_frame = imgp.get_frame(ImageProcessing.RED)
        cf = gbv.CircleFinder(gbv.EMPTY_PIPELINE, gbv.GameObject(1))
        l_white = cf.find_shapes_unsorted(white_frame)
        l_red = cf.find_shapes_unsorted(white_frame)
        print("Whites : {}".format(len(l_white)))
        print("Reds : {}".format(len(l_red)))

        cropped_frame = imgp.current_cropped_frame
        if not original.show_frame(cropped_frame):
            break
        if not white_filtered.show_frame(white_frame):
            break
        if not red_filtered.show_frame(red_frame):
            break


if __name__ == '__main__':
    main2()
