import cv2
from reciever import SecretCamera

import gbvision as gbv

# ColorThreshold([[176, 255], [198, 255], [155, 255]], 'RGB')

# ColorThreshold([[200, 255], [202, 255], [201, 255]], 'RGB') !!!WHITE ON BLACK!!!

ERODE_AND_DIALATE_DEFAULT = 30


class ImageProcessing:
    INTERPOLATION = cv2.INTER_CUBIC
    STDV = 45
    WHITE = "WHITE"
    RED = "RED"

    def __init__(self, camera, erode_and_dilate_size=ERODE_AND_DIALATE_DEFAULT, size=(1000, 1000)):
        self.camera = camera
        self.camera_init()
        self.window = gbv.CameraWindow('feed', camera)
        self.window.open()
        self.erode_and_dialate_size = erode_and_dilate_size
        self.size = size
        self.pipelines = {ImageProcessing.WHITE: None}
        self.bbox_bounds = [[], []]
        self.current_original_frame = None
        self.current_cropped_frames = [None, None]
        self.current_piped_frames = [None, None]

    def setup(self):
        self.next_frame()
        self.crop_init(0)
        self.crop_init(1)
        self.init_pipeline(ImageProcessing.WHITE)
        cv2.destroyAllWindows()

    def camera_init(self):
        pass

    def crop_init(self, box_index):
        frame = self.get_original_frame()
        self.bbox_bounds[box_index] = cv2.selectROI('feed', frame)

    def init_pipeline(self, color):
        # pipeline = gbv.ColorThreshold([[0, 100], [0, 255], [0, 255]], 'HSV')

        self.get_cropped_frames()
        bbox = cv2.selectROI('feed', self.current_cropped_frames[0])
        self.pipelines[color] = gbv.median_threshold(self.current_cropped_frames[0], ImageProcessing.STDV, bbox, 'RGB')
        print(self.pipelines[color])
        self.pipelines[color] += gbv.ErodeAndDilate(self.erode_and_dialate_size)
        return self.pipelines[color]

    def next_frame(self):
        ok, self.current_original_frame = self.camera.read()
        if not ok:
            raise NotImplementedError()

    def get_original_frame(self):
        return self.current_original_frame

    def get_cropped_frames(self):
        cropped_frames = []
        for i in range(len(self.bbox_bounds)):
            frame = gbv.crop(self.current_original_frame, *self.bbox_bounds[i])
            cropped_frames.append(cv2.resize(frame, self.size, interpolation=ImageProcessing.INTERPOLATION))
        self.current_cropped_frames = cropped_frames
        return self.current_cropped_frames

    def get_piped_frames(self, color):
        piped_frames = []
        for frame in self.current_cropped_frames:
            piped_frames.append(self.pipelines[color](frame))
        self.current_piped_frames = piped_frames
        return piped_frames

    def get_frames(self, color):
        self.get_original_frame()
        self.get_cropped_frames()
        return self.get_piped_frames(color)


class CircleFindWrapper:
    def __init__(self):
        self.circle_wrapper = gbv.CircleFinder(gbv.EMPTY_PIPELINE, gbv.GameObject(1))

    def get_count(self, white_frame, red_frame):
        l_white = self.circle_wrapper.find_shapes_unsorted(white_frame)
        l_red = self.circle_wrapper.find_shapes_unsorted(red_frame)
        l_white = [(x[0][0],x[0][1]) for x in l_white]
        l_red = [(x[0][0],x[0][1]) for x in l_red]
        return l_white, l_red


def setup_stage(camera):

    return None, None, None, None, None  # ret top bbox, bottom bbox, threshold, top reader, bottom reader


def wait_stage(proc, finder, top_reader, bot_reader):

    while True:
        top, _ = proc.get_frames()
        c_top = finder.get_count(top)
        if len(c_top) > 0:
            break
    time.sleep(8.0/25.0)

    top, bottom = proc.get_frames()
    circ_top, circ_bot = finder.get_count(top), finder.get_count(bottom)

    next = 0
    for cp in circ_top:
        next += 2 ** (top_reader.get_nearest(cp))
    for cb in circ_bot:
        next += 2 ** (4 + bot_reader.get_nearest(cb))

    time.sleep(5.0/25.0)

    return next  # returns message length when signal start


def read_stage(proc, finder, bytes_c, top_reader, bot_reader):

    ret = []
    for i in range(bytes_c):
        top, bottom = proc.get_frames()
        circ_top, circ_bot = finder.get_count(top), finder.get_count(bottom)

        next = 0

        for cp in circ_top:
            next += 2 ** (top_reader.get_nearest(cp))
        for cb in circ_bot:
            next += 2 ** (4 + bot_reader.get_nearest(cb))

        ret.append(next)

        time.sleep(5.0/25.0)

    return ret


def main():
    # s = SecretCamera(SecretCamera.ARAZI)
    circle_finder = CircleFindWrapper()
    # camera = gbv.USBCamera(0)
    camera = gbv.USBCamera(r"C:\Users\t8854535\Desktop\sprint2\test_data\total_test4.avi")
    # camera = s
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
        frame0, frame1 = imgp.get_frames(ImageProcessing.WHITE)
        l_0, l_1 = circle_finder.get_count(frame0, frame1)
        print("TOP: {}".format(l_0))
        print("BOTTOM: {}".format(l_1))

        #cropped_frames = imgp.current_cropped_frames
        if not original.show_frame(imgp.current_original_frame):
            break
        if not white_filtered.show_frame(frame0):
            break
        if not red_filtered.show_frame(frame1):
            break


if __name__ == '__main__':
    main()
