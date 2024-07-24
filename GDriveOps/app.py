from __future__ import print_function
import os
import re
import PyPDF2
import fitz
import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from docx import Document
import configparser
from GDriveOps.GDhandler import GoogleDriveHandler
import nltk
#from nltk.corpus import stopwords
#from nltk.tokenize import sent_tokenize, word_tokenize
#from nltk.stem import WordNetLemmatizer
import string
import openai
import streamlit as st
from langchain_openai import ChatOpenAI
import openai
from groq import Groq
from langchain.chains import LLMChain, RetrievalQA
#import time
#import re
import warnings
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.base import Runnable
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
import uuid
from datetime import datetime, timedelta
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from langchain.embeddings import HuggingFaceInstructEmbeddings
#from InstructorEmbedding import INSTRUCTOR
from sklearn.cluster import KMeans
import numpy as np
import voyageai
from langchain_voyageai import VoyageAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from rouge_score import rouge_scorer
from GDriveOps.GDhandler import GoogleDriveHandler



def main():
    st.title("PDF Research Paper Summarizer")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        with open("uploaded_file.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Generating summary..."):
            handler = GoogleDriveHandler(credentials_path='credentials.json')
            text = handler.extract_text_from_pdf("uploaded_file.pdf")
            combined_text, sections = handler.extract_sections(text)

            selected_model = st.sidebar.selectbox("Select a model", ["llama3-8b-8192", "llama3-70b-8192", "gpt-4o-mini", "gpt-4o", "gpt-4"])
            OPENAI_API_KEY = st.secrets["api_keys"]["OPENAI_API_KEY"]
            GROQ_API_KEY = st.secrets["api_keys"]["GROQ_API_KEY"]
            VOYAGEAI_API_key = st.secrets["api_keys"]["VOYAGE_AI_API_KEY"]

            summary = handler.summarize_text(combined_text, selected_model, OPENAI_API_KEY, GROQ_API_KEY, VOYAGEAI_API_key)

        st.subheader("Summary")
        st.write(summary)

        if st.button("Save Summary as DOCX"):
            output_path = os.path.join("summary_folder", "summary.docx")
            handler.save_summary_as_docx(summary, output_path)
            st.success(f"Summary saved to {output_path}")

if __name__ == "__main__":
    main()


