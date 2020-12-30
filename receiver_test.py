import gbvision as gbv
import time

from reciever import SecretCamera

asd = r"http://132.64.143.144:5000/video_feed"


def main():
    camera = gbv.USBCamera(SecretCamera.HELP)
    print(camera.get_fps())  # fps = 25
    window = gbv.RecordingCameraWindow(window_name='camera example', wrap_object=camera,
                                       file_name='aaaaa.avi',
                                       fps=6)
    window.show()
    camera.release()


if __name__ == '__main__':
    main()
