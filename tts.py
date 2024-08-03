from gtts import gTTS
import os


def text_to_speech(text, path="story.mp3", lang='en', tld="us"):
    obj = gTTS(text=text, lang=lang, slow=False, tld=tld)
    obj.save(path)


if __name__ == '__main__':
    print("Hello World")
    text_to_speech("Hello beautiful world!")
    os.system("play story.mp3")
