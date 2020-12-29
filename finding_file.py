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
            foo()
            drives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]
        x = _diff(drives, uncheckeddrives)
        if x:
            ham()
            drives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]


def find(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if "txt" in file:
                secret_file_name = file
                return (root + "\\" + secret_file_name)
