# Green Screen Video to Sequences of Alpha PNGs

This Python-based tool converts green screen videos into sequences of PNG files, replacing the green background with an alpha layer. This tool is particularly useful for importing videos into Lens Studio, as demonstrated in the following video: [Lens Studio Guide](https://www.youtube.com/watch?v=7kmFh8KtgEg)

## Prerequisites

The tool depends on the following Python libraries:
- PIL (pillow)
- numpy
- natsort
- cv2
- youtube_dl
- argparse
- argcomplete
- imageio
- numpngw
- APNGLib

## Installation

To install the necessary dependencies, run the provided shell script:

```bash
bash install.sh
```

## Usage

### Converting a Green Screen Video to PNGs

To convert a YouTube video, use the following command:

```bash
python3 GreenVideotoAlphaPNGs.py https://www.youtube.com/watch?v=ybX4VuArZOQ
```

### Creating a Transparent (Alpha) GIF

First, set the `dir` variable in the main function to the desired folder name. 

To create a transparent GIF, use the following command:

```bash
python3 GIFGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha"
```

**Note**: GIF generation is quite slow due to the use of the APNGLib library, which is currently the only viable solution.

### Creating a Transparent (Alpha) Video (Work in Progress)

You can create a video with a custom speed (fps) using the following command:

```bash
python3 GIFGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha" --fps 24
```

## Lens Studio (Snapchat AR)

After generating the sequence of images, you can import them into Lens Studio:

1. Click on the Resources panel.
2. Choose Add New -> 2D animation from files -> Ok in the popup menu.
3. Adjust the settings for the imported object, including audio and cutout animation.

Alternatively, you can import the generated alpha GIF or video directly into Lens Studio.

![add 2D animation in lens studio](https://raw.githubusercontent.com/antoinebou13/GreenScreenVideotoAlphaPNGs/master/images/addanim.jpg "add 2D animation")

This Python-based tool simplifies the process of using green screen videos in Lens Studio, thereby facilitating the creation of immersive AR experiences.
