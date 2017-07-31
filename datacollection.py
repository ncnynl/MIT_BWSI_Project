import feedparser
import justext
import requests
import sys
from database import Database

from bs4 import BeautifulSoup, SoupStrainer
import re
# import html2text
# from markdown import markdown
import mistune

from unidecode import unidecode

# db = Database("database.pkl")

def get_text_from_reuters(link):
    response = requests.get(link)
    resText = response.content.decode("UTF-8", 'ignore')
    soup = BeautifulSoup(resText, 'lxml')
    tmp = [x.extract() for x in soup.find_all(class_= "Edition_items_293of")]
    for tag in soup.find_all(["script", "meta", "head", "style", "noscript"]):
        tag.decompose()
    for tag in soup.find_all(True, class_= ["Attribution_content_27_rw", "Image_container_1tVQo"]):
        tag.decompose()
    paragraphs = justext.justext(soup.prettify(), justext.get_stoplist("English"))
    text = "\n\n".join([p.text for p in paragraphs if not p.is_boilerplate])
    return text

def get_text_from_cnn(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'lxml')
    for tag in soup.find_all(["script","img", "meta", "head", "style", "noscript", "h3", "h4"]):
        tag.decompose()
    for tag in soup.find_all(class_= ["video__end-slate__top-wrapper", "cd__headline", "el__storyelement--standard","el__article--embed", "zn-body__read-more", "el__leafmedia","el__leafmedia--storyhighlights", "zn-body__footer", "el__embedded--standard", "el__storyelement__title", "media__caption"]):
        tag.decompose()
    title = soup.find("h1", class_ = "pg-headline")
    content = soup.find("section", id = "body-text")

    return "{}\n\n{}".format(title.get_text(), content.get_text())

def get_text_from_wikipedia(link):
    markdown = mistune.Markdown()
    response = requests.get(link)
    # print("got a response", flush = True)
    unaccented_string = unidecode(str(response.content)).replace("\\n", " ")
    # print("removed accents", flush = True)
    html = unaccented_string
    html = markdown(html)
    # print("got markdown", flush = True)
    strained = SoupStrainer()
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find(id = "firstHeading")
    content = soup.find("div", class_ = "mw-parser-output")
    to_remove = content.find(id = "External_links")
    to_remove = content.find(id = "Notes") if content.find(id = "Notes") is not None else to_remove
    to_remove = content.find(id = "See_also") if content.find(id = "See_also") is not None else to_remove
    to_remove = content.find(id = "Gallery") if content.find(id = "Gallery") is not None else to_remove
    to_remove = content.find(id = "Selected_bibliography") if content.find(id = "Selected_bibliography") is not None else to_remove
    if to_remove is not None:
        parent = list(to_remove.parents)[0]
        for tag in parent.find_next_siblings(): 
            tag.decompose()

    for tag in content.find_all(["math", "table", "h2", "sup"]):
        tag.decompose()
    for tag in content.find_all(True, id = ["toc"]):
        tag.decompose()
    for tag in content.find_all(True, class_ =["mw-editsection", "quotebox", "infobox", "vertical-navbox", "navbox", "reference", "reflist", "thumb"]):
        tag.decompose()
    for tag in content.find_all(True, role = "note"):
        tag.decompose()

    # print(title)
    # print(content)

    return "{}\n\n{}".format(title.get_text(), content.get_text())

def collect(url, source):
    # read RSS feed
    #link: http://feeds.reuters.com/reuters/topNews
    d = feedparser.parse(url)
    # grab each article
    texts = {}
    for entry in d["entries"]:
        link = entry["link"]
        print("downloading: " + link)
        text = source(link)
        texts[link] = text
    return texts
    
# https://www.reuters.com/tools/rss
# http://feeds.reuters.com/Reuters/domesticNews
# db = Database("database.pkl")
# sourceToFunc={}
# sourceToFunc['reuters'] = get_text_from_reuters
# sourceToFunc['cnn'] = get_text_from_cnn
# url = sys.argv[1]
# source = sys.argv[2].lower()

# texts = collect(url, sourceToFunc[source])
# for l in texts:
#     print(l)
#     db.addDocument(l, texts[l])


