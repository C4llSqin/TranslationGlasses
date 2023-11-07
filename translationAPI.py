#!usr/bin/env python3

#import requests
#import json
import googletrans


#TRANSLATE_ENDPOINT = "https://libretranslate.com/translate"
#TRANSLATE_ENDPOINT = "http://192.168.137.206:5000/translate"
#TRANSLATE_ENDPOINT = googletrans.Translator()

def translate(q: str, source: str = "auto", destination: str = "en") -> dict[str, str]:
    translator = googletrans.Translator()
    return translator.translate(q, destination, source).text

if __name__ == "__main__":
    inputtext = input("Translate Text> ")
    source = input("Source[auto]> ")
    target = input("Dest[en]> ")
    if source=="": source = "auto"
    if target=="": target = "en"
    print(f"Returned: {translate(inputtext, source, target)}")
