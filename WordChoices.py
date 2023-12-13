import streamlit as st
import openai
import json
import pandas as pd

user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """
            If the given text has vocabularies that have synonyms or antonyms, 
            list the vocabularies in a JSON array, one vocabulary per line. 
            Each vocabulary should have 4 fields :
            - "Vocabulary" - The vocabulary
            - "Meaning" - Thai translation of the vocabulary.
            - "Synonyms" - synonyms of the vocabulary.
            - "Antonyms" - antonyms of the vocabulary.
        """    


st.title('Word choices')
st.markdown("Give us some passage. We will find some interesting vocabularies and give you their synonyms and antonyms!")
st.image('synonyms-antonyms.png')

user_input = st.text_area("Enter some text here:")


if st.button('Submit'):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far
    )
    
    st.markdown('**Here is some interesting vocabularies!**')
    vocabularies_dict = response.choices[0].message.content

    vocabs = json.loads(vocabularies_dict)

    print (vocabs)
    response_dataframe = pd.DataFrame.from_dict(vocabs)
    print(response_dataframe)
    st.table(response_dataframe)