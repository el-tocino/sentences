## what the heck?
Takes a bunch of subdirectories of mp3 files, convert them to wavs, transcribe the audio contained, compare to source material.

## the things
  
You'll need sox to convert and clip the audio files.  Requirements.txt has the python pieces you'll need listed.  I've left deepspeech and the server bit off of that, you might not want to run those parts on the same host. 

split.sh converts audio files from mp3 to 16k mono wav files, and then splits that based on silence.  findsource.py compares the transcription to the source sentences and adds its tops three guesses to that file.  

I used deep speech since I had it setup, and pushing 40+hours of audio through google's api was going to start costing me. It's running on an nvidia 1030 with an i7-4770.  It handles about 11 sentences/queries a minute, slightly slower than real time. A better card would increase the speed, of course. Once I get the sentences aligned with the source text may try retraining the model...hah.  Just not on a 1030.

### examplings

A bash for loop handled all the directories with audio:
```
for i in $(find . -maxdepth 1 -type d |grep -v '.'$)
do
cd $i
    for j in $(ls *.mp3)
    do
    ../split.sh $j
    done
done
```
And for the transcribing:

```for i in $(ls *.wav)
do
curl -x POST --data-binary @${i} http://deepspeech:1880/stt > ${i}.txt
done
```

And the comparing of source to transcription:

```
/tools/findsource.py /path/to/source.txt /path/to/transcription/text/files/
```

The script will update the transcription text files with the top 3 guesses that it pulls from the source text sentences.  It works on a directory at a time since it parses the source text into discrete sentences for comparing.  Doing that once per file would be a time suck.

### references

[Sox](http://sox.sourceforge.net/sox.html)

[Deepspeech Server](https://github.com/MainRo/deepspeech-server)

[Deepspeech](https://github.com/mozilla/DeepSpeech)

[My cheesy Deepspeech Server Scripts](https://github.com/el-tocino/DSSS)

### comments/questions/updates/rude remarks?

File a pr!
