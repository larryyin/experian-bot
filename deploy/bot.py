import os
import openai
import gradio as gr
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationTokenBufferMemory
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']
hf_api_key = os.environ['HF_API_KEY']

host = os.environ['PGVECTOR_HOST']
port = os.environ['PGVECTOR_PORT']
database_name = os.environ['PGVECTOR_DATABASE']
user = os.environ['PGVECTOR_USER']
passwd = os.environ['PGVECTOR_PASSWD']

bot_name = "Experian Bot V0.2"
bot_desc = "Experian's chatbot, from its public webcrawl, serves a credit feast for all."

embedding = OpenAIEmbeddings()

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver="psycopg2",
    host=host,
    port=int(port),
    database=database_name,
    user=user,
    password=passwd,
)

COLLECTION_NAME = "experian230725"

vectordb = PGVector(embedding_function=embedding,
                  collection_name=COLLECTION_NAME,
                  connection_string=CONNECTION_STRING,
                 )

# llm_name = "gpt-3.5-turbo"
llm_name = "gpt-3.5-turbo-16k"
# llm_name = "gpt-4-32k"
llm = ChatOpenAI(model_name=llm_name, temperature=0)

retriever=vectordb.as_retriever()
memory = ConversationTokenBufferMemory(
    llm = llm,
    max_token_limit=8000,
    memory_key="chat_history",
    return_messages=True
)
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory,
    verbose=False
)

with gr.Blocks() as demo:
    gr.Markdown(f"# {bot_name}\n\n{bot_desc}")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Type your message (Shift + Enter to submit)", lines=6)
    submit = gr.Button("Submit")
    clear = gr.Button("Clear")

    def respond(message, chat_history):
        result = qa({"question": message})
        chat_history.append((message, result["answer"]))
        return ("", chat_history)

    msg.submit(respond, [msg, chatbot], [msg, chatbot], queue=False)
    submit.click(respond, [msg, chatbot], [msg, chatbot], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)

gr.close_all()
demo.queue()
demo.launch(share=True)

# gr.close_all()
# demo.close()
# demo.clear()
