from pmb.utils import centroid_histogram, get_colors
from sklearn.cluster import MiniBatchKMeans
import cv2
import time
import numpy as np
from tqdm import tqdm
from dateutil.relativedelta import relativedelta as rd


def frame_iter(capture, description):
    def _iterator():
        while capture.grab():
            yield capture.retrieve()[1]

    return tqdm(_iterator(), desc=description, total=int(capture.get(cv2.CAP_PROP_FRAME_COUNT)), )


def process_images(file, title, subtitle, width=1920, height=1080, path='videos'):
    # Start the timer
    start_time = time.time()

    # Start the Video Capture
    cap = cv2.VideoCapture('%s/%s' % (path, file))

    # Calculate some stats of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = round(length / fps, 2)
    to_shift = round(width / duration, 2)

    # Title Text Vars
    font_title = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_title = (50, (height - 50))
    font_scale_title = 2
    font_color_title = (255, 255, 255)
    line_type_title = 2

    # Subtitle Text Vars
    font_subtitle = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_subtitle = (50, (height - 25))
    font_scale_subtitle = 1
    font_color_subtitle = (255, 255, 255)
    line_type_subtitle = 2

    # Init Counters
    count = 0
    start_x = 0

    # Format the Time output
    fmt = '{0.days} days {0.hours} hours {0.minutes} minutes {0.seconds} seconds'

    # Create the resulting image
    barcode = np.zeros((height, width, 3), dtype="uint8")

    # Loop through every frame
    for frame in frame_iter(cap, 'Progress'):

        # On first iteration show the stats
        # Does not work in every console
        count += 1
        if count == 1:
            print("FPS:%s, Total Frames:%s, Length in Seconds:%s, Bars (%s/%s):%s" % (
                fps, length, duration, width, duration, to_shift))

        # Convert Image every second
        if count % fps == 0:

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = image.reshape((image.shape[0] * image.shape[1], 3))

            clt = MiniBatchKMeans(n_clusters=1, max_iter=10, n_init=1)
            clt.fit(image)
            hist = centroid_histogram(clt)
            color = get_colors(hist, clt.cluster_centers_)

            # Set the width of the colored bar
            end_x = start_x + to_shift
            cv2.rectangle(barcode, (int(start_x), 0), (int(end_x), height), color, -1)
            start_x = end_x

        pass

    # Release the Video Capture
    cap.release()

    # Convert the image back to RGB Colors
    barcode = cv2.cvtColor(barcode, cv2.COLOR_BGR2RGB)

    # Save the image
    cv2.imwrite("result/%s.jpg" % file, barcode)

    # Put the Title text on the image
    cv2.putText(barcode, title,
                bottom_left_title,
                font_title,
                font_scale_title,
                font_color_title,
                line_type_title)

    # Put the Subtitle text on the image
    cv2.putText(barcode, subtitle,
                bottom_left_subtitle,
                font_subtitle,
                font_scale_subtitle,
                font_color_subtitle,
                line_type_subtitle)

    # Save the second image with text
    cv2.imwrite("result/%s_text.jpg" % file, barcode)

    # Print the elapsed time
    print(fmt.format(rd(seconds=round((time.time() - start_time), 0))))