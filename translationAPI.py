import requests
import json

#TRANSLATE_ENDPOINT = "https://libretranslate.com/translate"
TRANSLATE_ENDPOINT = "https://localhost:5000/translate"

def translate_with_source_and_dest(q: str, source: str, destination: str) -> dict[str, str]:
    data = {
        "q": q,
        "source": source,
        "target": destination
    }
    res = requests.post(TRANSLATE_ENDPOINT, data)
    return json.loads(res.text)

def translate_to_dest(q: str, destination: str = "en") -> dict[str, str]:
    data = {
        "q": q,
        "source": "auto",
        "target": destination
    }
    res = requests.post(TRANSLATE_ENDPOINT, data)
    return json.loads(res.text)

if __name__ == "__main__":
    inputtext = input("Translate Text> ")
    source = input("Source[auto]> ")
    target = input("Source[en]> ")
    if source=="": source = "auto"
    if target=="": target = "en"
    print(f"Returned: {translate_with_source_and_dest(inputtext, source, target)}")
