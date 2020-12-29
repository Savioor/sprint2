

class MultiLedReader:

    def __init__(self, raw_led_locs):
        raw_led_locs_by_x = sorted(raw_led_locs, key=lambda p: p[1])
        raw_led_locs_by_y = sorted(raw_led_locs, key=lambda p: p[1])

        diff_x = raw_led_locs_by_x[-1] - raw_led_locs_by_x[0]
        diff_y =  raw_led_locs_by_y[-1] - raw_led_locs_by_y[0]

        locs_sorted = []
        if diff_x > diff_y:
            locs_sorted = raw_led_locs_by_x
        else:
            locs_sorted = raw_led_locs_by_y

        self.start = locs_sorted[0]
        self.end = locs_sorted[-1]

    def get_shadow(self, point):
        pass

