#!/bin/bash

NFN=$(echo $1 | sed s/.mp3//)
ffmpeg -i $1 -acodec pcm_s16le -ac 1 -ar 16000 ${NFN}.wav
sox  ${NFN}.wav ${NFN}_split.wav silence 1 0.1 1% 1 .66 1% : newfile : restart
rm ${NFN}.wav