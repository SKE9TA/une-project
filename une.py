import streamlit as st
from docx import Document
import requests
import re
import openai


def get_extracted_text(doc_path):
    response = requests.post('http://localhost:5000/extract-text', json={'docPath': doc_path})
    headers={'Content-Type': 'application/json'}
    data = {'doc_path': doc_path}
    response = requests.post(response, headers=headers, json=data)
    return response.json()['text']

def get_parsed_translations(text):
    response = requests.post('http://localhost:5000/parse-translations')
    headers={'Content-Type': 'application/json'}
    response = requests.post(response, headers=headers, json={'text':text})
    return response.json()

def get_find_information(text, query):
    response = requests.get('http://localhost:5000/find-information')
    headers={'Content-Type': 'application/json'}
    response = requests.post(response, headers=headers, json={'text':text, 'query':query})
    return response.json()

# Function to extract text from the document
def extract_text_from_word(doc_path):
    text = ''
    try:
        doc = Document(doc_path)
        for para in doc.paragraphs:
            text += para.text + '\n'
        return text
    except Exception as e:
        return f"Error: {e}"
    
# Function to parse translations from the document text
def parse_translations(text):
    translations = {}
    lines = text.split('\n')
    for line in lines:
        if ':' in line:
            term, translation = map(str.strip, line.split(':', 1))
            translations[term.lower()] = translation
    return translations    

# Modified find_information function to first search in the document and then use OpenAI
def find_information(text, query):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    relevant_sentences = [sentence for sentence in sentences if query.lower() in sentence.lower()]
    if relevant_sentences:
        response = ' '.join(relevant_sentences)
        return response, len(response)
    else:
        # Fallback to OpenAI if no direct match is found
        response = openai.Completion.create(
          engine="gpt-3.5-turbo-0125",
          prompt=f"Answer the following question: '{query}'",
          max_tokens=1000,
          n=1,
          stop=None,
          temperature=0.5,
        ).choices[0].text.strip()
        return response, len(response)
openai.api_key = 'YOUR_API_KEY'

def main():
    st.title("AI Terminologies Chatbot")
    doc_path = 'AI TERMINOLOGIES AND THEIR TRANSLATIONS.docx'

    # Extract text from the document
    doc_text = extract_text_from_word(doc_path)
    translations= parse_translations(doc_path)    
    # Ask user for a query
    user_query = st.text_input("Ask me anything about AI terminologies:")

    print(user_query)

    if user_query:
        response, response_length = find_information(doc_text, user_query)
        st.write(f"***Response***: {response}")
        #st.write(f"***Length of Response***: {response_length}")

if __name__ == "__main__":
    main()
