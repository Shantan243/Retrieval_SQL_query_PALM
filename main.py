from langchain_helper import get_few_shot_db_chain

import streamlit as st

st.title("SQL Query Retrieval system")

question = st.text_input("Question: ")
if question:
    new_chain = get_few_shot_db_chain()
    answer = new_chain.run(question)
    st.header("Answer:")
    st.write(answer)
