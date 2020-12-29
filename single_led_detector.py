import cv2
import numpy as np
from reciever import SecretCamera

import gbvision as gbv

s = SecretCamera(SecretCamera.ARAZI)

# ColorThreshold([[176, 255], [198, 255], [155, 255]], 'RGB')

# ColorThreshold([[200, 255], [202, 255], [201, 255]], 'RGB') !!!WHITE ON BLACK!!!

ERODE_AND_DIALATE_DEFAULT = 30

class ImageProcessing:
    INTERPOLATION = cv2.INTER_CUBIC
    STDV = 45
    WHITE = "WHITE"
    RED = "RED"

    def __init__(self, camera, erode_and_dilate_size=ERODE_AND_DIALATE_DEFAULT, size=(1000,1000)):
        self.camera = camera
        self.camera_init()
        self.window = gbv.CameraWindow('feed', camera)
        self.window.open()
        self.erode_and_dialate_size = erode_and_dilate_size
        self.size = size
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
        print(self.pipelines[color])
        self.pipelines[color] += gbv.ErodeAndDilate(self.erode_and_dialate_size)
        return self.pipelines[color]

    def next_frame(self):
        ok, self.current_original_frame = self.camera.read()
        if not ok:
            raise NotImplementedError()

    def get_original_frame(self):
        return self.current_original_frame

    def get_cropped_frame(self):
        frame = gbv.crop(self.current_original_frame, *self.bbox_bound)
        self.current_cropped_frame = cv2.resize(frame, self.size, interpolation=ImageProcessing.INTERPOLATION)
        return self.current_cropped_frame

    def get_piped_frame(self, color):
        return self.pipelines[color](self.current_cropped_frame)

    def get_frame(self, color):
        self.get_original_frame()
        self.get_cropped_frame()
        return self.get_piped_frame(color)

class CircleFindWrapper:
    def __init__(self):
        self.circle_wrapper = gbv.CircleFinder(gbv.EMPTY_PIPELINE, gbv.GameObject(1))

    def get_count(self, white_frame, red_frame):
        l_white = self.circle_wrapper.find_shapes_unsorted(white_frame)
        l_red = self.circle_wrapper.find_shapes_unsorted(red_frame)
        return l_white, l_red

def main():

    circle_finder = CircleFindWrapper()

    #camera = gbv.USBCamera(0)
    camera = gbv.USBCamera(r"C:\Users\t8854535\Desktop\sprint2\test_data\total_test3.avi")
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
        l_white, l_red = circle_finder.get_count(white_frame, red_frame)
        print("Whites: {}".format(l_white))
        print("Reds: {}".format(l_red))

        cropped_frame = imgp.current_cropped_frame
        if not original.show_frame(cropped_frame):
            break
        if not white_filtered.show_frame(white_frame):
            break
        if not red_filtered.show_frame(red_frame):
            break


if __name__ == '__main__':
    main()
