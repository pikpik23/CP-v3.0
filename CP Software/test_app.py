from app import *
from glob import glob
import os
import shutil

print(glob("/Volumes/*"))


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def save():
    files = glob("/Volumes/*")

    rem = ["/Volumes/student", "/Volumes/com.apple.TimeMachine.localsnapshots", "/Volumes/Macintosh HD", "Blah"]

    for path in rem:
        try:
            files.remove(path)
        except ValueError:
            pass

    print(files)

    usb = None
    for path in files:
        if "CP" in path:
            usb = os.path.join(path, "Backup")
        else:
            usb = None
            print("No Backup USB found")

    if usb:
        # save to usb
        print("Saving...")
        save(os.path.join(usb, "files"), "resources/files")
        save(os.path.join(usb, "db"), "resources/static/db")
        print("...Saved")

def save(dest, src):
    if not os.path.exists(dest):
        os.makedirs(dest)
        copytree(src, dest)

if __name__ == '__main__':
    save()