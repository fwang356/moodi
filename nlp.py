import lyricsgenius
import nltk
from langdetect import detect
from deep_translator import GoogleTranslator
from nltk.sentiment import SentimentIntensityAnalyzer
from client import gcid, gsecret, token

genius = lyricsgenius.Genius(token)
stopwords = nltk.corpus.stopwords.words("english")
sia = SentimentIntensityAnalyzer()


def lyrics(title, artist):
    song = genius.search_song(title, artist)
    if song == None:
        return "Not Found"
    string = song.lyrics.replace("EmbedShare", "")
    string = string.replace("URLCopyEmbedCopy", "")

    length = len(string)
    string = string[0:length - 1]
    length -= 1
    while string[length - 1].isdigit() or string[length - 1] == '' or string[length - 1] == '\n':
        string = string[0:length - 1]
        length -= 1
    
    return string


def clean(string):    
    string = string.replace('[', "1")
    string = string.replace(']', "1")

    string = GoogleTranslator(source="auto", target="en").translate(string)

    lyrics = string.split('\n')
    
    for i in range(len(lyrics)):
        lyrics[i] = nltk.word_tokenize(lyrics[i])
        lyrics[i] = [w for w in lyrics[i] if w.isalpha()]
        lyrics[i] = [w for w in lyrics[i] if w.lower() not in stopwords]
        lyrics[i] = ' '.join(lyrics[i])
    
    lyrics = [phrase for phrase in lyrics if phrase != '']

    return lyrics


def analyze(lyrics):
    total = 0
    for phrase in lyrics:
        total += sia.polarity_scores(phrase)["compound"]

    score = total/len(lyrics) + 1
    score *= 50
    return score