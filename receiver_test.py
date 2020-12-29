import gbvision as gbv
import time

from reciever import SecretCamera


def main():
    camera = gbv.USBCamera(SecretCamera.ARAZI)
    print(camera.get_fps())  # fps = 25
    original = gbv.FeedWindow(window_name='original')
    # camera.manually_bound()
    # window = gbv.RecordingCameraWindow(window_name='camera example', wrap_object=camera,
    #                                    file_name='total_test4.avi',
    #                                    fps=camera.get_fps())
    # time.sleep(5)
    # [camera.read() for i in range(100)]
    while True:
        original.show_frame(camera.read()[1])
    camera.release()


if __name__ == '__main__':
    main()