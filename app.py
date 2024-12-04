import os
import streamlit as st
import openai
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables in a file called .env
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('MODEL_NAME')  # Sử dụng mô hình đã được định nghĩa trong .env

# Function to summarize transcript content
def summarize_content(transcript):
    system_prompt = """You are an GraphRAG export and working as professor at Harvard University tasked with teaching lessons on Knowledge Graphs for RAG System. 
    Generate a lesson with detailed knowledge for GraphRAG based on the content of the transcript/your knowledge.
    Additionally, generate a few review questions based on the content of the lesson."""
    
    user_prompt = f"Transcript content: {transcript}\n\n. "

    response = openai.ChatCompletion.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message['content']

# Function to process chat-based follow-up questions
def ask_follow_up(question, conversation_history):
    system_prompt = "You are a helpful assistant that provides answers to follow-up questions based on the previous conversation."
    
    # Include conversation history to maintain context
    messages = [{"role": "system", "content": system_prompt}]
    for entry in conversation_history:
        messages.append({"role": entry['role'], "content": entry['content']})
    
    # Add the user's new question to the chat
    messages.append({"role": "user", "content": question})
    
    response = openai.ChatCompletion.create(
        model=openai_model,
        messages=messages
    )
    return response.choices[0].message['content']


# Function to convert the summary content to a README-like text file
def convert_to_text_file(content):
    return content.encode()

# Streamlit app interface
st.title("Graph RAG Professor")
# Text area for inputting transcript
transcript = st.text_area("Paste your transcript here")

# Sidebar information
with st.sidebar:
    st.header("Lam Hoang Cat Vy")
    st.subheader("IT - Young Talents - VPBank")
    st.write("**Actual working roles:** Business Analyst, System Analyst, CloudOps, Python Developer, Automation Test Developer, Tester")
    st.write("**Email:** vylhc@vpbank.com.vn | catvyisworking@gmail.com")
    st.write("**Contact:** 0898177342")

# If transcript is provided, process it
if transcript:
    try:
        # Generate summary, code example, and review questions
        summary_response = summarize_content(transcript)
        st.write("Generated Lecture:")
        st.write(summary_response)  # Display the generated content

        # Initialize conversation history
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        
        # Add the system's response to the conversation history
        st.session_state.conversation_history.append({"role": "assistant", "content": summary_response})

        # Download the entire summary as a README-like text file
        text_file_data = convert_to_text_file(summary_response)
        st.download_button(label="📥 Download full response as README", 
                           data=text_file_data, 
                           file_name="README.txt", 
                           mime="text/plain")
        
    #     # Chat section
    #     st.write("### Ask Follow-up Questions:")
    #     user_question = st.text_input("Ask a question based on the content")
        
    #     if user_question:
    #         # Add the user's question to the conversation history
    #         st.session_state.conversation_history.append({"role": "user", "content": user_question})
            
    #         # Get the follow-up response from OpenAI
    #         follow_up_response = ask_follow_up(user_question, st.session_state.conversation_history)
            
    #         # Display the response
    #         st.write(f"**Assistant:** {follow_up_response}")
            
    #         # Add the assistant's response to the conversation history
    #         st.session_state.conversation_history.append({"role": "assistant", "content": follow_up_response})

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please paste your transcript.")
