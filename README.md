# Green Screen Video to Sequences of Alpha PNGs

Green Screen Video to sequence of PNGs files replacing the green by an alpha layer in python3

I made this from making easier to import video in lens studio after watching this video:

https://www.youtube.com/watch?v=7kmFh8KtgEg

## Dependencies

    PIL (pillow)
    numpy
    natsort
    cv2
    youtube_dl
    argparse
    argcomplete
    imageio

## Using the script

```bash
python3 GreenVideotoAlphaPNGs.py https://www.youtube.com/watch?v=ybX4VuArZOQ
```

### For making alpha gif or jif easier (W.I.P)
Change in the main the dir variable by the folder name, but not alpha yet

```bash
python3 GIFGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha"
```

### For making alpha video (W.I.P)
Create video with a custom speed(fps), but not alpha yet

```bash
python3 GIFGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha" --fps 24
```

## from Lens Studio (Snapchat AR) 

After generating the sequence of images just click in Resources panel
Add New -> 2D animation from files -> Ok in the popup menu
change the setting for those object
- audio
- cutout animation

![add 2D animation in lens studio](https://raw.githubusercontent.com/antoinebou13/GreenScreenVideotoAlphaPNGs/master/images/addanim.jpg "add 2D animation")
