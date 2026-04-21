import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from Backend.BaseClass import BaseClass
from Backend.state import State
import re
import requests
from bs4 import BeautifulSoup

class Querycleaner(BaseClass):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def execute(self, state:State):
        query=state["query"]
        link=state["link"]
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser") 

        title_tag = soup.find("title")  
        if title_tag:
            title = title_tag.text.strip() 
        else:
            title = "Unknown Title"

        state["vedioTitle"] = title
        
        query = query.lower()
        query = re.sub(r'\s+', ' ', query).strip()
        # Process with spaCy
        doc = self.nlp(query)
        # Remove stopwords, punctuation, and lemmatize words
        cleaned_tokens = [
            token.lemma_
            for token in doc
            if not token.is_stop and not token.is_punct and token.lemma_.isalpha()
        ]

        # Join cleaned tokens back into string
        cleaned_query = ' '.join(cleaned_tokens)
        state["Cleanedquery"]=cleaned_query
        state["TitledQuery"]=state["vedioTitle"]+" "+state["Cleanedquery"]
        return state

# state={
#     "query":"What is this Video is Explaining?"
# }
# cleaner=Querycleaner()
# print(cleaner.execute(state=state))