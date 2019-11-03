## what the heck?
This takes a bunch of subdirectories of mp3 files, convert them to wavs, transcribe the audio contained, compare to source material in prep for building a tacotron data model.  It sort of manually works. I've been running it against a librivox chapter to refine the process. Should also refine the scripts more and make them a bit more cohesive eventually. 

Also now adding ramblings about things that pop up for historical amusement.

### the things
  
You'll need sox to convert and clip the audio files.  Requirements.txt has the python pieces you'll need listed.  I've left deepspeech and the server bit off of that, you may not want to run those parts on the same host, or you might have a better solution.

split.sh converts audio files from mp3 to 16k mono wav files, and then splits that based on silence.  findsource.py compares the transcription to the source sentences and adds its tops three guesses to that file.  

I used deep speech since I had it setup, and pushing 40+hours of audio through google's api was going to start costing me. It's running on an nvidia 1030 with an i7-4770 with 4gb of RAM and a slow spindle hd (update: with 8gb and an SSD it's about 8-12/min. update 2: DS .2.0 is much faster, though accuracy suffers).  It handles about 10 sentences/queries* a minute, slightly slower than real time. A better card would increase the speed, of course. Once I get the sentences aligned with the source text may try retraining the model.....just not on a 1030.

* a single sentence in my case averages 5 seconds of clearly recorded English. 

### the stuff

make some waves:
```
split.sh dirnamehereornot
```

for the transcribing:

```
cd wavs/
for i in $(ls *.wav)
  do
  curl -x POST --data-binary @${i} http://deepspeech:1880/stt > ../${i}.txt
done
```

And the comparing of source to transcription:

```
/tools/findsource.py /path/to/source.txt /path/to/transcription/text/files/
```

The script will update the transcription text files with the top guess that it pulls from the source text sentences.  It works on a directory at a time since it parses the source text into discrete sentences for comparing.  Doing that once per file would be a time suck.

### knobs to tweak

The silence length is probably the big one.  I found a happy medium for the material I was using.  It hits about 80% of sentence break points on the material I used.  Some bits would probably benefit from a more fine-tuned length.  It's quick on any modern machine, so don't be afraid to try changing the value to fit your source audio ( .66 in split.sh is the value I have now).

### travails

Deepspeech doesn't like to start translating at the very beginning or end of a file.  Adding a bit of silence to each wav improved my transcriptions.  As there's inconsistent silence in the source material, doing it as a separate step here makes a slight bit more sense than trying to retain the source silences.  And one more quirk about all this, if you're feeding these to tacotron type models, you'll want to create padded copies and retain the originals.  Make sure you keep the two separate...

make some silence:
```
sox -n -r 16000 -b 16 -c 1 silence.wav trim 0.0 0.3
```
create padded copies:
```
export SILWAV=/opt/tacotron/data/silence.wav
mkdir padded
for i in $(ls *.wav) ; do
sox ${SILWAV} ${i} ${SILWAV} padded/${i}
done
```

Source material with non-standard words will still require a lot of manual adjustment.  

After parsing large source wav/mp3's, check the length of those files to be sure:
```
exiftool -Duration *.wav > durations
```

Project Gutenberg source texts are frequently trimmed to 80-character lines, which ends up with a bunch of \n bits in the middle of lines. There's probably a beautiful soup way to re-frame that to untrimmed paragraphs before it gets fed to the matching.  

There's a number of short (<1s) files ("end of chapter") that crop up.  These should be removed or combined with other short files to make longer files.  
```
sox -n -r 16000 -b 16 -c 1 space.wav trim 0.0 0.15
sox shortwav1.wav space.wav shortwav2.wav new.wav
```
be sure to edit the txt files as well.  

### references

[Sox](http://sox.sourceforge.net/sox.html)

[Deepspeech Server](https://github.com/MainRo/deepspeech-server)

[Deepspeech](https://github.com/mozilla/DeepSpeech)

[My cheesy Deepspeech Server Scripts](https://github.com/el-tocino/DSSS)

[exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/)

[Project Gutenberg](https://www.gutenberg.org/)

[Librivox](https://librivox.org/)

### comments/questions/updates/rude remarks?

File a pr!
