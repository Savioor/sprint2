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

    def __init__(self, camera):
        self.camera = camera
        self.camera_init()
        self.window = gbv.CameraWindow('feed', camera)
        self.window.open()
        self.pipeline = None
        self.bbox_bound = None
        self.current_original_frame = None
        self.current_cropped_frame = None
        self.current_piped_frame = None

    def camera_init(self):
        self.camera.set_exposure(-5)
        self.camera.resize(.1, .1)

    def crop_init(self):
        frame = self.get_original_frame()
        self.bbox_bound = cv2.selectROI('feed', frame)

    def init_pipeline(self, *temp_args):
        # pipeline = gbv.ColorThreshold([[0, 100], [0, 255], [0, 255]], 'HSV')
        pipeline = gbv.median_threshold(*temp_args)
        print(pipeline)
        # pipeline += gbv.ErodeAndDilate(2)
        return pipeline

    def get_original_frame(self):
        ok, self.current_original_frame = self.camera.read()
        return self.current_original_frame

    def get_cropped_frame(self):
        frame = gbv.crop(self.current_original_frame, *self.bbox_bound)
        self.current_cropped_frame = cv2.resize(frame, (800, 800), interpolation=ImageProcessing.INTERPOLATION)
        return self.current_cropped_frame

    def get_piped_frame(self):
        return get_pipeline()(self.current_cropped_frame)

    def get_frame(self):
        self.get_original_frame()
        self.get_cropped_frame()
        return self.get_piped_frame()



def get_pipelined_window_stream(pipeline):
    return gbv.FeedWindow(window_name='after threshold', drawing_pipeline=pipeline)


def show_pipelined_video(frame, pipeline):
    return get_pipelined_window_stream(pipeline).show_frame(frame)


def get_pipeline(*temp_args):
    # pipeline = gbv.ColorThreshold([[0, 100], [0, 255], [0, 255]], 'HSV')
    pipeline = gbv.median_threshold(*temp_args)
    print(pipeline)
    # pipeline += gbv.ErodeAndDilate(2)
    return pipeline


def get_hidden_camera():
    return


def main():
    # camera = gbv.USBCamera(0)
    camera = gbv.USBCamera(r"C:\Users\t8854535\Desktop\sprint2\test_data\record.avi")
    imgp = ImageProcessing(camera)
    imgp.crop_init()
    imgp.init_pipeline()


def main2():
    # camera = gbv.USBCamera(0)
    camera = gbv.USBCamera(r"C:\Users\t8854535\Desktop\sprint2\test_data\green_led.avi")
    camera.set_exposure(-5)
    camera.resize(.1, .1)
    window = gbv.CameraWindow('feed', camera)
    window.open()

    frame = window.show_and_get_frame()
    bbox_bound = cv2.selectROI('feed', frame)

    interpol = cv2.INTER_CUBIC

    frame = gbv.crop(window.show_and_get_frame(), *bbox_bound)
    frame = cv2.resize(frame, (1000, 1000), interpolation=interpol)

    cv2.destroyAllWindows()

    original = gbv.FeedWindow(window_name='original')

    while True:
        ok, frame = camera.read()
        frame = gbv.crop(frame, *bbox_bound)
        frame = cv2.resize(frame, (800, 800), interpolation=interpol)
        original.show_frame(frame)
        k = original.last_key_pressed
        if k == 'r':
            bbox = cv2.selectROI('original', frame)
            pipeline = get_pipeline(frame, stdv, bbox, 'RGB')
            # thr = gbv.ColorThreshold([[0,100], [0,255], [0,255]], 'HSV')
            break
    cv2.destroyAllWindows()

    print(pipeline)

    original = gbv.FeedWindow(window_name='original')
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=pipeline)

    original.open()
    after_proc.open()
    while True:
        ok, frame = camera.read()
        frame = gbv.crop(frame, *bbox_bound)
        frame = cv2.resize(frame, (800, 800), interpolation=interpol)
        if not original.show_frame(frame):
            break
        if not after_proc.show_frame(frame):
            break

    original.close()
    after_proc.close()


if __name__ == '__main__':
    main()
