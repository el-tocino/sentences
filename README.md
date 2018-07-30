
needs sox installed and python needs nltk.  nltk will need to download the tokenizer the first time, import nltk into python and then run "nltk.download()" and follow the instructions.  

The various parts here convert audio files from mp3 to 16k mono wav files, then split them based on silence.  findsource.py compares the transcription to the source sentences and adds its tops three guesses to that file.  

https://github.com/MainRo/deepspeech-server
https://github.com/mozilla/DeepSpeech
I have a repo with my startup scripts for DSS somewhere...
