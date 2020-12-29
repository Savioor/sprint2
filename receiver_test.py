import gbvision as gbv
import time

from reciever import SecretCamera


def main():
    camera = gbv.USBCamera(SecretCamera.DANIEL)
    print(camera.get_fps())  # fps = 25
    window = gbv.RecordingCameraWindow(window_name='camera example', wrap_object=camera,
                                       file_name='final10-03.avi',
                                       fps=6)
    window.show()
    camera.release()


if __name__ == '__main__':
    main()