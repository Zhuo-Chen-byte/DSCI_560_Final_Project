import streamlit as st
import pandas as pd
import os

from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from llama_index.embeddings import HuggingFaceEmbedding
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import CTransformers
from langchain import HuggingFacePipeline
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain

from support.htmlTemplates import css, bot_template, user_template
from dotenv import load_dotenv
from config import Config


load_dotenv()
config = Config()
os.environ['OPENAI_API_KEY'] = config.openai_api_key

recommended_companies_and_explanations = pd.read_csv(config.recommended_companies_and_explanations_filepath)
resume_template_images_metadata = pd.read_csv(config.resume_template_images_metadata_filepath)


def get_pdf_text(pdf_docs):
    text = ''
    
    for pdf_doc in pdf_docs:
        text += ''.join(page.extract_text() for page in PdfReader(pdf_doc).pages)
        
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    
    return text_splitter.split_text(text)


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

        
def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    llm = CTransformers(model='models/gpt2.bin', model_type='gpt2')
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 4}),
        memory=memory,
    )
    
    return conversation_chain


def show_question_and_answer(show_chat_history: bool) -> None:
    messages_to_display = st.session_state.chat_history[st.session_state.current_page * 2: st.session_state.current_page * 2 + 2]
    print(messages_to_display)
    
    if show_chat_history:
        st.write('**Question:**\n' + messages_to_display[0].content, unsafe_allow_html=True)
    
    st.write('**Answer:**\n' + messages_to_display[1].content, unsafe_allow_html=True)
    
    if not show_chat_history:
        st.markdown('''
            <style>
                .big-font {
                    font-size:50px !important;
                }
            </style>''',
        unsafe_allow_html=True)
        
        cheer_up = '<p class="big-font"> Fight on! You can find the job! </p>'
        st.markdown(cheer_up, unsafe_allow_html=True)


def generate_answer(user_question: str) -> None:
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    
    st.session_state.current_page = len(st.session_state.chat_history) // 2 - 1
    show_question_and_answer(False)


def main():
    load_dotenv()
    
    st.set_page_config(page_title="Let's help find your first full-time job!",
                       page_icon=':envelope_with_arrow:')
    
    st.write(css, unsafe_allow_html=True)

    if not 'conversation' in st.session_state:
        st.session_state.conversation = None
    if not 'chat_history' in st.session_state:
        st.session_state.chat_history = None
    if not 'current_page' in st.session_state:
        st.session_state.current_page = 0
    if not 'answer_chat' in st.session_state:
        st.session_state.display_chat = False
    
    st.header(':rainbow[Land your first job - Start Here] :envelope_with_arrow:')
    user_question = st.text_input('Ask questions based on your resume:')
    
    # Page-shift
    left_shift, _, right_shift = st.columns([1, 1, 1])
    
    if user_question:
        if st.button('Submit my question'):
            generate_answer(user_question)
            st.session_state.display_chat = True
        else:
            st.session_state.display_chat = False
    
    if st.session_state.chat_history and len(st.session_state.chat_history) > 2:
        with left_shift:
            if st.button('<'):
                if st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    
        with right_shift:
            if st.button('>'):
                if st.session_state.current_page < len(st.session_state.chat_history) // 2 - 1:
                    st.session_state.current_page += 1
        
        if not st.session_state.display_chat:
            show_question_and_answer(True)
            

    # Provide common questions for users
    st.markdown('''
        <style>
        .big-font {
        font-size:32px !important;
        }
        </style>''',
        unsafe_allow_html=True)

    st.markdown('<p class="big-font"> Common Questions </p>',
                unsafe_allow_html=True)

    if st.button('How can I improve my skills'):
        generate_answer('How can I improve my skills')
        st.session_state.display_chat = True

    if st.button('Evaluate my background'):
        generate_answer('Evaluate my background')
        st.session_state.display_chat = True
    
    if st.button('Recommend some tech companies that are likely to hire'):
        st.write('**Answer:**\n')
        st.write('A few recommended companies and their explanations are \n')
        
        for i in range(len(recommended_companies_and_explanations)):
            st.write(f'{recommended_companies_and_explanations.iloc[i, 0]}, which is {recommended_companies_and_explanations.iloc[i, 1]} \n')
    
    if st.button('Show some resume templates'):
        num_images, num_images_shown = len(resume_template_images_metadata), 0
        
        for i in range(num_images):
            try:
                st.write('\n\n\n**----------------------------------------------------- Resume Begins -----------------------------------------------------**\n\n\n')
                st.image(resume_template_images_metadata.iloc[i, 0], caption='url: ' + resume_template_images_metadata.iloc[i, 1])
                st.write('\n\n\n**------------------------------------------------------ Resume Ends ------------------------------------------------------**\n\n\n')
                
                num_images_shown += 1
            except:
                continue
            
            if num_images_shown >= 3:
                break
        
    
    # Side-bar to upload resumes
    with st.sidebar:
        st.subheader('Your Resume :clipboard:')
        
        pdf_docs = st.file_uploader("Upload your resume here and click on 'Analyze Your Resume'",
                                    accept_multiple_files=True)
            
        if st.button('Analyze Your Resume :memo:'):
            with st.spinner('Analyzing your resume ...'):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()
