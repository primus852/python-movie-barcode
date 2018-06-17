from calculate import process_images
from daemoniker import Daemonizer
from utils import str2bool
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-d', '--daemonize', type=str2bool, nargs='?', const=True, default=True, help='Run as Daemon')
parser.add_argument('-f', '--file', help='Path to file', required=True)
parser.add_argument('-w', '--width', help='Width of resulting image', default=1920, type=int)
parser.add_argument('-height', '--height', help='Height of resulting image', default=1080, type=int)
parser.add_argument('-p', '--path', help='Path the file is in', default='videos/')
parser.add_argument('-vt', '--video_title', help='Title of Video', default='')
parser.add_argument('-vs', '--video_subtitle', help='Subtitle of Video', default='')

args = parser.parse_args()

if args.daemonize:
    with Daemonizer() as (is_setup, daemonizer):
        is_parent = daemonizer('runs.pid')

process_images(args.file, args.video_title, args.video_subtitle, args.width, args.height, args.path)

