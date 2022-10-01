#!/bin/python3

import sys
import os
import ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def splitCSV(file):
    games = []
    for line in file:
        games.append([s.strip() for s in line.split(',')])
    return games

def findMP4():
    for path in os.listdir():
        if ".mp4" in path:
            return path # really bad code
    return False

# takes string s in (hh:)(mm:)ss format and converts it to an int in seconds
def timeToSec(s):
    nums = s.split(':')
    nums.reverse() # reverse so the enumeration works

    # this is kinda like sci-notation for the time
    seconds = 0
    for i, num in enumerate(nums):
        seconds += int(num)*(60**i) # works, probably slow, shut up
    return seconds

def main():

    with open("matches.csv") as r:
        matches = splitCSV(r)
        name = matches[0][0]
        try:
            os.mkdir(name)
        except FileExistsError:
            print("Directory " + name + " already created")

    video = findMP4()
    if video == False:
        print("No video found in directory, quitting...")
        return 1
    path = name + '/' + video
    os.rename(video, path)
    os.chdir(name)
    os.mkdir("matches")

    for i,game in enumerate(matches):
        if i == 0:
            continue
        title = f"%s %s VS %s - %s"%(str(i).zfill(2), game[2], game[3], game[1]) # I LOVE F STRINGS !!!!!
        # 01 P1 VS P2 - WF
        # game list: start, match, p1, p2, end 
        start = game[0]
        end = game[4]
        print(f"'%s': %s-%s" % (title, start, end))
        ffmpeg_extract_subclip(video, timeToSec(start), timeToSec(end), "matches/" + title + ".mp4")
    os.rename("../quick-vod/matches.csv", "matches.csv")
    print("Finished")

if __name__ == "__main__":
    main()
