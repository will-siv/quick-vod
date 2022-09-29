# quick-vod

i got tired of cutting VODs in premiere to upload individual matches on to youtube because it took too much time. these tools help to make that process easier without having to use an editor.

## dependencies:

- twitch-dl
- ffmpeg
- moviepy
- tkinter

(i dont know how to do this automatically)

## vodmaker.py

REALLY GOOD NAME for a tool that allows me to enter the times, names, and match for a youtube VOD

## split.py

splits videos based on a csv made by `vodmaker.py`

## setup.sh

main script; downloads VOD from twitch channel (unless told not to), then splits said VOD into parts in a named directory

all of this is a mess - i have little plans to organize it unless i go insane over how bad it is

## using the tool

clone the repo into the folder that the VOD folders will be

```console
$ ls
Tournament 1    Tournament 2    quick-vod
```

` python3 quick-vod/vodmaker.py `

opens a tkinter gui to create individual VODs from a single video in a directory

` quick-vod/setup.sh [-s] [channelname] `

`-s`: skip download, for if you have a video already in the directory


