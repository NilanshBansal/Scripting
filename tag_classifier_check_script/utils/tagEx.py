from flashtext import KeywordProcessor
import os 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


keyword_processor = KeywordProcessor()

with open(BASE_DIR+"/utils/keywords") as keywords:
    for keyword in keywords.readlines():
        keyword_processor.add_keyword(keyword.strip())

def tagEx(data):
    try:
        keywords_found = keyword_processor.extract_keywords(data)
    except Exception as e:
        return "ERR"

    return list(set(keywords_found))


