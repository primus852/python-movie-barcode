from pmb import calculate as c
from daemoniker import Daemonizer
from pmb.utils import str2bool
from argparse import ArgumentParser


if __name__ == '__main__':

    # Parse Arguments
    parser = ArgumentParser()
    parser.add_argument('-d', '--daemonize', type=str2bool, nargs='?', const=True, default=False, help='Run as Daemon')
    parser.add_argument('-f', '--file', help='Path to file', required=True)
    parser.add_argument('-w', '--width', help='Width of resulting image', default=1920, type=int)
    parser.add_argument('-height', '--height', help='Height of resulting image', default=1080, type=int)
    parser.add_argument('-p', '--path', help='Path the file is in', default='videos/')
    parser.add_argument('-o', '--output', help='Path the file result should be saved', default='result/')
    parser.add_argument('-vt', '--video_title', help='Title of Video', default='')
    parser.add_argument('-vs', '--video_subtitle', help='Subtitle of Video', default='')

    # Collected Arguments
    args = parser.parse_args()

    # Daemonize if per arg
    if args.daemonize:
        with Daemonizer() as (is_setup, daemonizer):
            is_parent = daemonizer('runs.pid')

    # Read the video and process the images
    c.process_images(args.file, args.video_title, args.video_subtitle, args.width, args.height, args.path)
