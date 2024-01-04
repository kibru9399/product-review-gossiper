import streamlit as st
from script import chain
import os
import json
from utils import *
from script import *
@st.cache_resource
def start_qa():
    chaine = chain()
    return chaine.make_qa()


qa = start_qa()

 
# App title
with st.sidebar:
    st.title('🦙💬 Your Product Gossiper')
    st.write('This chatbot will help you understand hundreds of reviews of ur product so u can make informed decision')
 
    # Create a dictionary to store categories and their items

    with open('grouped_titles.json', 'r') as f:
        categories = json.load(f)
    with open('topics4vis.json', 'r') as f:
        d2= json.load(f)
    # Create the first dropdown for main categories
    main_category = st.selectbox("Select a Category", categories.keys())

    # Create the second dropdown for items within the selected category
    if main_category:
        items = categories[main_category]
        selected_item = st.selectbox("Select an Item", items)

        # Display the selected item
        if selected_item:
            st.write("You selected:", selected_item)

    st.pyplot(topic_vis(d2[selected_item]))

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

replicate_api = 2
# def invoke(prompt_input):
#     global qa
#     return qa.run(prompt_input)
# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt) 
text = f"### for the product {selected_item}: {prompt} "
# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"): 
        with st.spinner("Thinking..."): 
            response = qa({"query": text})
            placeholder = st.empty() 
            full_response = response['result']
             
            placeholder.markdown(full_response)
            
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
