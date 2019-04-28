import os
import imageio
import datetime
from PIL import Image
from natsort import natsorted, ns

import cv2
import numpy as np

import argcomplete
import argparse

# python3 VideoGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha"

def create_video(directory, fps=30, color_array=[45, 255, 8]):
    output_file = 'Videogen-%s.mov' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    if os.path.isdir(directory):
        images = [img for img in natsorted(os.listdir(directory),alg=ns.PATH) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(directory, images[0]))
        height, width, layers = frame.shape

        os.system("ffmpeg -i %s -vf %s -c copy -c:v png output.mov" % (directory, "chromakey=0x70de77:0.1:0.2"))
        
        # video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), float(fps), (width, height))

        # for image in images:
          # array_image = cv2.imread(os.path.join(directory, image), cv2.IMREAD_UNCHANGED)
          # array_image = cv2.cvtColor(array_image, cv2.COLOR_RGBA2BGR)
          # video.write(array_image)

        # cv2.destroyAllWindows()
        # video.release()

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
