import cv2
import numpy as np
from reciever import SecretCamera

import gbvision as gbv

s = SecretCamera(SecretCamera.DANIEL)

stdv = np.array([20, 80, 80])

def get_pipelined_window_stream(pipeline):
    return gbv.FeedWindow(window_name='after threshold', drawing_pipeline=pipeline)

def show_pipelined_video(frame, pipeline):
    return get_pipelined_window_stream(pipeline).show_frame(frame)


def get_pipeline(*temp_args):
    # pipeline = gbv.ColorThreshold([[0, 100], [0, 255], [0, 255]], 'HSV')
    pipeline = gbv.median_threshold(*temp_args)
    print(pipeline)
    #pipeline += gbv.ErodeAndDilate(2)
    return pipeline

def main():
    camera = gbv.USBCamera(0)
    #camera = gbv.USBCamera(r"C:\Users\t8854535\Desktop\sprint2\capture2.PNGrr")
    camera.set_exposure(-5)
    window = gbv.CameraWindow('feed', camera)
    window.open()
    while True:
        frame = window.show_and_get_frame()
        k = window.last_key_pressed
        if k == 'r':
            bbox = None  # checks whole frame
            bbox = cv2.selectROI('feed', frame)
            pipeline = get_pipeline(frame, stdv, bbox, 'HSV')
            #thr = gbv.ColorThreshold([[0,100], [0,255], [0,255]], 'HSV')
            break
    cv2.destroyAllWindows()

    print(pipeline)



    original = gbv.FeedWindow(window_name='original')
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=pipeline)

    original.open()
    after_proc.open()
    while True:
        ok, frame = camera.read()
        if not original.show_frame(frame):
            break
        if not after_proc.show_frame(frame):
            break

    original.close()
    after_proc.close()


if __name__ == '__main__':
    main()
