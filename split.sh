#!/bin/bash

# convert the files in an existing directory to consumable chunks for deepspeech.  

# adjust as necessary...
BITRATE=16000
MAXDUR=11.00

if [[ $# -eq 1 ]] ; then
  SOURCEDIR=$1
else
  SOURCEDIR=$(pwd)
fi

# setup directory structure if it doesn't exist.
# sanity...
if [[ ! -d "${SOURCEDIR}" ]] ; then
  echo "No source directory to work in, exiting!"
  exit 10
fi

if [[ ! -d wavs ]] ; then
  mkdir wavs
fi

if [[ ! -d tmp ]] ; then
  mkdir tmp
fi

if [[ ! -d padded ]] ; then
  mkdir padded
fi

# conjunction functions...

split_wav() {
  sox  $1 $2 silence 1 0.1 1% 1 $3 1% : newfile : restart
}


# go to work

if cd "${SOURCEDIR}" ; then
  echo "Starting to make waves."
else
  echo "can't access ${SOURCEDIR}?"
  exit 11
fi

# split things up...
for mp3file in $(ls *.mp3) ; do
  WBN=$(echo $mp3file | sed s/.mp3//)
  ffmpeg -i $mp3file -acodec pcm_s16le -ac 1 -ar $BITRATE ${WBN}.wav
  split_wav "${WBN}" "wavs/${WBN}" ".66"  
  mv ${WBN}.wav tmp/
  mv $mp3file tmp/
done

# get durations, re-trim lengthy ones...

exiftool -Duration wavs/*.wav > tmp/durations

for wtime in $(grep ^Duration tmp/durations | cut -d: -f2 | cut -d' ' -f2); do
  if (( $( echo "$wtime > $MAXDUR" | bc -l ) )) ; then
    REDO=$(grep -B1 "$wtime s" tmp/durations | grep -v ^Duration | cut -d' ' -f2)
    split_wav "$REDO" "$REDO" ".35"
    mv "$REDO" tmp/
  fi
done

# make padded copies...

sox -n -r 16000 -b 16 -c 1 tmp/silence.wav trim 0.0 0.4
SILWAV="tmp/silence.wav"

for wavs in $(ls wavs/*.wav) ; do
  PFN=$(echo "${wavs}" | sed s/wavs/padded/)
  sox "${SILWAV}" "${WAVS}" "${SILWAV}" "${PFN}"
done
