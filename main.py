import json

from stopwords import stopwords
from krwordrank.word import KRWordRank
from wordcloud import WordCloud
from PIL import Image

def generate_keywords(file_path):
    texts = []

    with open(file_path, encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        json_comments_data = json_data["comments"]

        for comments in json_comments_data:
            if comments["headline"] != None: texts.append(comments["headline"])
            if comments["review"] != None: texts.append(comments["review"])

    wordrank_extractor = KRWordRank(min_count = 5, max_length = 10)
    keywords, rank, graph = wordrank_extractor.extract(texts, beta = 0.85, max_iter = 10)

    for word in stopwords:
        keywords.pop(word)

    return keywords

def generate_wordcloud(keywords):
    wordcloud = WordCloud(
        width = 800,
        height = 800,
        font_path = "fonts/JejuGothic.ttf",
        background_color="white",
    )
    
    wordcloud = wordcloud.generate_from_frequencies(keywords)
    image = Image.fromarray(wordcloud.to_array())
    
    return image

if __name__ == "__main__":
    file_name = "닌텐도 스위치 모여봐요 동물의 숲 한국어 게임타이틀"

    keywords = generate_keywords("input/" + file_name + ".json")
    image = generate_wordcloud(keywords)
    image.save("result/" + file_name + ".jpeg")