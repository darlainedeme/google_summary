import requests
from bs4 import BeautifulSoup
import nltk
import streamlit as st
from googlesearch import search

# Set the query that you want to search for
sentence = st.sidebar.text_input('Write your research query:', value='government policies energy 2022') 

n = 10

for url in search(sentence, stop=n, lang="en"):
    reqs = requests.get(url)
    text = BeautifulSoup(reqs.text, 'html.parser').get_text()
    summary = nltk.summarize(text)
    st.write(summary)
