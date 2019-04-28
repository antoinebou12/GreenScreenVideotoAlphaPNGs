#!/usr/bin/env bash
#youtube-dl latest
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
#APNGLib install
cd lib/APNGLib_fix
python3 setup.py install --user
cd ../..
#requirements
pip3 install -r requirements.txt
