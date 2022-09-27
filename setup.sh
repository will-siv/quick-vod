#!/bin/bash

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

if [[ -n $1 ]]; then
    CHANNEL=$1
else
    echo "usage: setup [-s] channel"
    exit 1
fi

if [[ -z "$SKIP" ]]; then
    twitch-dl videos --no-color $CHANNEL | grep --color=never "Video " > /tmp/ids
    sed -i 's/Video //g' /tmp/ids

    if [[ -d temp ]]; then
        rm -rf temp/*
    else
        mkdir temp
    fi
    cd temp
    num=0
    touch files.tmp
    cat /tmp/ids | while read line; do
        if grep -q $line ../.ids; then # tests if line is in file
            echo "Already downloaded ID $line, skipping."
        else
            echo $line >> ../.ids # append id
            num=`expr $num + 1`
            twitch-dl download -q 1080p60 $line -o ${num}.mp4
            echo ${num}.mp4 >> files.tmp
        fi
    done

    num=`ls *.mp4 | wc -l`
    if [ "$num" -eq 0 ]; then
        echo No videos downloaded.
    elif [ "$num" -eq 1 ]; then
        mv 1.mp4 out.mp4
    else
        ffmpeg -f concat -safe 0 -i files.tmp -c copy out.mp4
    fi
    mv out.mp4 ..
    cd ..
    rm -rf temp
    rm /tmp/ids
fi

# do python stuff first
./split.py

