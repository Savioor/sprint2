import os
import os.path


def _diff(list1, list2):
    list_difference = [item for item in list1 if item not in list2]
    return list_difference


dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
drives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]


def _check_usb():
    global drives
    while True:
        uncheckeddrives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]
        x = _diff(uncheckeddrives, drives)
        if x:
            return x[0]
        x = _diff(drives, uncheckeddrives)
        if x:
            drives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]


def find():
    path = _check_usb()
    valid_files = []
    for root, dirs, files in os.walk(path):
        if len(root) < 3:
            for file in files:
                if file[-4:] in (".txt", ".bmp"):
                    valid_files.append(root + "\\" + file)
    valid_files.sort(key=lambda f: os.stat(f).st_size, reverse=True)
    return list(reversed(valid_files))[1:]
