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
    numpngw
    APNGLib

## Using the script

- [X] Make it work
- [ ] Better sort for the file (order)
- [ ] Threading

```bash
python3 GreenVideotoAlphaPNGs.py https://www.youtube.com/watch?v=ybX4VuArZOQ
```

### For making transparent gif or jif  (W.I.P)
Change in the main the dir variable by the folder name
I used a the APNGLib to create the transparent gif. It is slow, but i didn't found a other solution for now
Installed the [APNGLib](https://github.com/slicer4ever/APNGLib) in the same named directory with

```bash
python3 setup.py install --user 
```

- [X] Make it work
- [ ] Threading
- [X] Make sure the gif is in alpha

```bash
python3 GIFGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha"
```

### For making alpha video (W.I.P)
Create video with a custom speed(fps)

- [X] Make it work
- [ ] Threading
- [ ] Make sure the video is in alpha

```bash
python3 GIFGenerator.py "Joker from Persona 5 Default Dance (Green Screen)-ybX4VuArZOQ_alpha" --fps 24
```

## Lens Studio (Snapchat AR) 

After generating the sequence of images just click in Resources panel
Add New -> 2D animation from files -> Ok in the popup menu
change the setting for those object
- audio
- cutout animation

![add 2D animation in lens studio](https://raw.githubusercontent.com/antoinebou13/GreenScreenVideotoAlphaPNGs/master/images/addanim.jpg "add 2D animation")
