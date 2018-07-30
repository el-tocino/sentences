
needs sox installed and python needs nltk.  nltk will need to download the tokenizer the first time, import nltk into python and then run "nltk.download()" and follow the instructions.  

split.sh converts audio files from mp3 to 16k mono wav files, and then splits that based on silence.  findsource.py compares the transcription to the source sentences and adds its tops three guesses to that file.  

Sox:
http://sox.sourceforge.net/sox.html
Deepspeech Server:
https://github.com/MainRo/deepspeech-server
Deepspeech:
https://github.com/mozilla/DeepSpeech

