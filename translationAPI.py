#!usr/bin/env python3

import requests
import json

#TRANSLATE_ENDPOINT = "https://libretranslate.com/translate"
TRANSLATE_ENDPOINT = "http://localhost:5000/translate"

def translate(q: str, source: str = "auto", destination: str = "en") -> dict[str, str]:
    data = {
        "q": q,
        "source": source,
        "target": destination
    }
    res = requests.post(TRANSLATE_ENDPOINT, data)
    return json.loads(res.text)

if __name__ == "__main__":
    inputtext = input("Translate Text> ")
    source = input("Source[auto]> ")
    target = input("Dest[en]> ")
    if source=="": source = "auto"
    if target=="": target = "en"
    print(f"Returned: {translate(inputtext, source, target)}")
