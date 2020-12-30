

class MultiLedReader:

    def __init__(self, raw_led_locs):
        raw_led_locs_by_x = sorted(raw_led_locs, key=lambda p: p[0])
        raw_led_locs_by_y = sorted(raw_led_locs, key=lambda p: p[1])

        diff_x = raw_led_locs_by_x[-1][0] - raw_led_locs_by_x[0][0]
        diff_y = raw_led_locs_by_y[-1][1] - raw_led_locs_by_y[0][1]

        locs_sorted = []
        if diff_x > diff_y or True:
            locs_sorted = raw_led_locs_by_x
        else:
            locs_sorted = raw_led_locs_by_y

        self.start = locs_sorted[0]
        self.end = locs_sorted[-1]
        self.diff = (self.end[0] - self.start[0], self.end[1] - self.start[0])
        self.shadows = [self.get_shadow(p) for p in locs_sorted]

    def get_shadow(self, point):
        x = self.diff[0]
        y = self.diff[1]
        size = x*x + y*y
        return (x*(point[0] - self.start[0]) + y*(point[1] - self.start[1]))/size

    def get_nearest(self, point):
        shadow = self.get_shadow(point)
        best_index = 0
        best = abs(self.shadows[0] - shadow)
        for i in range(len(self.shadows)):
            curr = abs(self.shadows[i] - shadow)
            if curr < best:
                best = curr
                best_index = i
        return best_index


if __name__ == "__main__":
    test = MultiLedReader([(1, 1), (3, 3)])
    print(test.get_shadow((1, 1)))
    print(test.get_shadow((2, 2)))
    print(test.get_shadow((3, 3)))
    print(test.get_nearest((2.98, 3.05)))

