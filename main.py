from sklearn.cluster import KMeans
import utils
import cv2
import time
import numpy as np
from tqdm import tqdm
from dateutil.relativedelta import relativedelta as rd


def frame_iter(capture, description):
    def _iterator():
        while capture.grab():
            yield capture.retrieve()[1]
    return tqdm(
        _iterator(),
        desc=description,
        total=int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
    )


start_time = time.time()
title = "breaking_bad.mp4"
width = 1920
height = 1080
cap = cv2.VideoCapture('mp4/%s' % title)
fps = cap.get(cv2.CAP_PROP_FPS)
length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
duration = length / fps
count = 0
to_shift = width / duration
utils.clear()

fmt = '{0.days} days {0.hours} hours {0.minutes} minutes {0.seconds} seconds'

start_x = 0

barcode = np.zeros((height, width, 3), dtype="uint8")


for frame in frame_iter(cap, 'Progress'):

    count += 1

    if count == 1:
        print("FPS:%s, Total Frames:%s, Length in Seconds:%s, Bars (%s/%s):%s" % (
            fps, length, duration, width, duration, to_shift))

    # Convert Image every second
    if count % fps == 0:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        clt = KMeans(n_clusters=1)
        clt.fit(image)
        # cv2.imshow('Video', frame)

        hist = utils.centroid_histogram(clt)

        color = utils.get_colors(hist, clt.cluster_centers_)
        end_x = start_x + to_shift
        cv2.rectangle(barcode, (int(start_x), 0), (int(end_x), height), color, -1)
        start_x = end_x

        percent = round(100 * count / length, 2)
        # utils.clear()
        # tqdm(percent, desc='Test', total=100)

        # print("Progress %s%%" % percent)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    pass

cap.release()

barcode = cv2.cvtColor(barcode, cv2.COLOR_BGR2RGB)
cv2.imwrite("result/%s.jpg" % title, barcode)
cv2.destroyAllWindows()
print(fmt.format(rd(seconds=round((time.time() - start_time), 0))))
