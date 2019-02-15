import os
import imageio
import datetime
from PIL import Image
from natsort import natsorted, ns

import argcomplete
import argparse

# python3 GIFGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha"

def create_gif(directory):
    if os.path.isdir(directory):
        images = [img for img in natsorted(os.listdir(directory), alg=ns.PATH) if img.endswith(".png")]
        for filename in images:
            if filename.endswith(".png"): 
                images.append(Image.open("{}/{}".format(directory, filename)).convert('RGBA'))
                
    output_file = 'Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    imageio.mimsave(output_file, images)
    
    
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