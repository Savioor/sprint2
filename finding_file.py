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
    for root, dirs, files in os.walk(path):
        files.sort(key=lambda f: os.stat(f).st_size, reverse=True)
        return root, files[0]
