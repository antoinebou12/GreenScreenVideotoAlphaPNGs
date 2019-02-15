import os
import imageio
import datetime
from PIL import Image
from natsort import natsorted, ns

import cv2

import argcomplete
import argparse

# python3 VideoGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha"

def create_video(directory, fps=30):
    output_file = 'Video-%s.avi' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    if os.path.isdir(directory):
        images = [img for img in natsorted(os.listdir(directory),alg=ns.PATH) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(directory, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(output_file, 0, float(fps), (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(directory, image)))

        cv2.destroyAllWindows()
        video.release()

if __name__ == "__main__":
    def _parser():
        parser = argparse.ArgumentParser(
            description="Create gif with a sequences of images")
        parser.add_argument('dir', type=str, help='directory of the all the image files')
        parser.add_argument('--fps',default=30, type=int, help='frame per second for the output video')
        return parser


    parser = _parser()
    argcomplete.autocomplete(parser)
    args = _parser().parse_args()

    create_video(args.dir, args.fps)