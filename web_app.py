import requests
from bs4 import BeautifulSoup
import nltk
import streamlit as st
from googlesearch import search
import heapq
import re
import io
import PyPDF2
from gensim.summarization import summarize

nltk.download('punkt')
nltk.download('stopwords')


# Set the query that you want to search for
sentence = st.sidebar.text_input('Write your research query:', value='uk energy subsidies reform 2022') 
n = st.sidebar.number_input("Define the extent of the research", min_value=1, max_value=10, value=2)

i = 0
for url in search(sentence, stop=n, lang="en"):
    i += 1
    if url.endswith('.pdf'):
        r = requests.get(url)
        f = io.BytesIO(r.content)

        pdf_reader = PyPDF2.PdfFileReader(f)
        # Read the PDF file
        article_text = ""
        for page in range(pdf_reader.numPages):
            article_text += pdf_reader.getPage(page).extractText()
            
    
    else:
        reqs = requests.get(url)
        parsed_article = BeautifulSoup(reqs.text, 'html.parser')
        paragraphs = parsed_article.find_all('p')
        
        article_text = ""
        
        for p in paragraphs:
            article_text += p.text

    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )    
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]


    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)

    # summary = nltk.summarize(text)
    st.write(i)
    try:
        st.write(parsed_article.find_all('title')[0].get_text())
    except:
        st.write("Title not foud")

    if url.endswith('.pdf'):
        st.write('PDF document:')
        
    st.write("source [link]({0})".format(url))
    
    st.write(summary)
