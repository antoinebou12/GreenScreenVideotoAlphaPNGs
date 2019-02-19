import os
import imageio
import numpngw
import numpy
import APNGLib
import datetime
from PIL import Image
from natsort import natsorted, ns

import argcomplete
import argparse

# python3 GIFGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha"

def create_gif(directory):
    if os.path.isdir(directory):
        images_name = [img for img in natsorted(os.listdir(directory), alg=ns.PATH) if img.endswith(".png")]
        all_images = []
        for filename in images_name: 
            all_images.append(numpy.array(Image.open("{}/{}".format(directory, filename)).convert('RGBA')))
    
    w, h, d = all_images[0].shape
    output_file = '%s.gif' % directory
    numpngw.write_apng(output_file, all_images, delay=50)
    APNGLib.MakeGIF(output_file, "dir.gif", 0)
    
if __name__ == "__main__":

    def _parser():
        parser = argparse.ArgumentParser(
            description="Create gif with a sequences of images")
        parser.add_argument('dir', type=str, help='directory of the all the image files')
        return parser


    parser = _parser()
    argcomplete.autocomplete(parser)
    args = _parser().parse_args()


    create_gif(args.dir)
