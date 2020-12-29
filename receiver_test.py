import gbvision as gbv

from reciever import SecretCamera


def main():
    camera = SecretCamera(SecretCamera.DANIEL)
    print(camera.get_fps())  # fps = 25
    # camera.manually_bound()
    window = gbv.RecordingCameraWindow(window_name='camera example', wrap_object=camera,
                                       file_name='total_test4.avi',
                                       fps=camera.get_fps())
    window.show()
    camera.release()


if __name__ == '__main__':
    main()