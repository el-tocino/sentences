Takes a bunch of subdirectories of mp3 files, convert them to wavs, transcribe the audio contained, compare to source material.  
You'll need sox to convert and clip the audio files.  Requirements.txt has the python pieces you'll need listed.  I've left deepspeech and the server bit off of that, you might not want to run those parts on the same host. 

split.sh converts audio files from mp3 to 16k mono wav files, and then splits that based on silence.  findsource.py compares the transcription to the source sentences and adds its tops three guesses to that file.  

A bash for loop handled all the directories with audio:

for i in $(find . -maxdepth 1 -type d |grep -v '.'$)
do
cd $i
    for j in $(ls *.mp3)
    do
    ../split.sh $j
    done
done

And for the transcribing:
for i in $(ls *.wav)
do
curl -x POST --data-binary @${i} http://deepspeech:1880/stt > ${i}.txt
done


Sox:
http://sox.sourceforge.net/sox.html
Deepspeech Server:
https://github.com/MainRo/deepspeech-server
Deepspeech:
https://github.com/mozilla/DeepSpeech
My cheesy Deepspeech Server Scripts:
https://github.com/el-tocino/DSSS

