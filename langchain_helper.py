from langchain.llms import GooglePalm
import google.generativeai as genai
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
import os
from few_shot import fewshots
from dotenv import load_dotenv
load_dotenv()

def get_few_shot_db_chain():
    llm = GooglePalm(google_api_key=os.environ["google_api_key"], temperature=0.2)
    db_user = "root"
    db_password = "Kautilya1414"
    db_host = 'localhost'
    db_name = 'atliq_tshirts'

    uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    db = SQLDatabase.from_uri(uri)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-V2')
    vectorize = [" ".join(example.values()) for example in fewshots]
    vectorstore = Chroma.from_texts(vectorize, embeddings, metadatas=fewshots)
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion:{Question}\nSQLQuery:{SQLQuery}\nSQLResult:{SQLResult}\nAnswer:{Answer}"
    )
    few_shot_temp = FewShotPromptTemplate(example_selector=example_selector,
                                          example_prompt=example_prompt,
                                          prefix=_mysql_prompt,
                                          suffix=PROMPT_SUFFIX,
                                          input_variables=["input", "table_info", "top_k"])
    new_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_temp)
    return new_chain

if __name__ == "__main__":
    new_chain =  get_few_shot_db_chain()
    print(new_chain.run("how many white color Levi t-shirts we have?"))
