#!/bin/bash

max_length=10.0
split_wav() {
  sox ${i} ${i} silence 1 0.1 1% 1 .5 1% : newfile : restart
  mv $i toobig
} 

for i in $(ls *.wav) ; do 
  duration=$(exiftool -Duration $i | cut -d: -f2 | sed s/s// | sed s/\ //g)
  if [[ "$duration" = 0 ]] ; then
    echo "duration is 0, splitting?"
    split_wav 
  fi
  TL=$(echo "$duration > $max_length" | bc -l)
  if [[ $TL = 1 ]] ; then
    echo "duration over 10s, splitting?"
    split_wav
  fi
done

