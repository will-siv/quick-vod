#!/bin/bash

# intended to be used in the directory that the video folders will be placed

# this is 'how not to write a bash script but i'm learning shut up'
# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash :)

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--skipdownload)
            SKIP=YES
            shift
            ;;
        -*|-**)
            echo "Unknown option $1"
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

set -- "${POSITIONAL_ARGS[@]}"

if [[ -z "$SKIP" ]]; then
    if [[ -n $1 ]]; then
        CHANNEL=$1
    else
        echo "usage: setup [-s] channel"
        exit 1
    fi
    mkdir /tmp/quickvod
    twitch-dl videos --no-color $CHANNEL | grep --color=never "Video " > /tmp/quickvod/ids
    sed -i 's/Video //g' /tmp/quickvod/ids

    num=0
    touch /tmp/quickvod/files
    cat /tmp/quickvod/ids | while read line; do
        if grep -q $line .ids; then # tests if line is in file
            echo "Already downloaded ID $line, skipping."
        else
            echo $line >> .ids # append id
            num=`expr $num + 1`
            twitch-dl download -q 1080p60 $line -o /tmp/quickvod/${num}.mp4
            echo "/tmp/quickvod/${num}.mp4" >> /tmp/quickvod/files
        fi
    done

    num=`ls /tmp/quickvod/*.mp4 | wc -l`
    if [ "$num" -eq 0 ]; then
        echo No videos downloaded.
    elif [ "$num" -eq 1 ]; then
        mv /tmp/quickvod/1.mp4 out.mp4
    else
        ffmpeg -f concat -safe 0 -i /tmp/quickvod/files -c copy out.mp4
    fi
    rm -rf /tmp/quickvod
fi

# i dont know a more clean way to run this other than putting it at the end of the script
# should this just be run by the user?
quick-vod/split.py

