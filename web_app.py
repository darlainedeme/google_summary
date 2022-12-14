import requests
from bs4 import BeautifulSoup
import nltk
import streamlit as st


# Set the query that you want to search for
sentence = st.sidebar.text_input('Write your research query:', value='government policies energy 2022') 

# Use requests to search for the query on Google
response = requests.get(f"https://www.google.com/search?q={sentence}")

# Use BeautifulSoup to parse the HTML response
soup = BeautifulSoup(response.text, "html.parser")

# Find the relevant results on the page
results = soup.find_all("title")

# Open each result in a new tab
for result in results:
    link = result.find("a")["href"]
    requests.get(f"http://www.google.com{link}")

# Use nltk to summarize the content of each page
for result in results:
    link = result.find("a")["href"]
    response = requests.get(f"http://www.google.com{link}")
    text = BeautifulSoup(response.text, "html.parser").get_text()
    summary = nltk.summarize(text)
    st.write(summary)
