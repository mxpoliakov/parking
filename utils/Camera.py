import threading
from time import time
from shutil import copyfile
import os


class Camera:
    def __init__(self, config):
        self.delay = 10
        self.last_photo_time = time() - self.delay

        self.src_dir = "images"
        self.dst_dir = "images_camera"
        self.run = True

    def check_to_make_photo(self):
        while self.run:
            if time() - self.last_photo_time > self.delay:
                self.take_next = True

    def photographer(self):
        i = 0
        while True:
            if not self.take_next: continue
            self.take_next = False
            self.last_photo_time = time()

            try:
                file_to_copy = os.listdir(self.src_dir)[i]
            except:
                self.run = False
                break
            i += 1
            if file_to_copy[-4:] != ".jpg":
                print("bad format")
                continue

            copyfile(os.path.join(self.src_dir, file_to_copy),
                     os.path.join(self.dst_dir, file_to_copy))

    def start(self):
        print("start camera")
        self.thread = threading.Thread(target=self.check_to_make_photo)
        self.thread.start()
        self.photographer()


if __name__ == "__main__":
    cam = Camera(1)
    cam.start()
