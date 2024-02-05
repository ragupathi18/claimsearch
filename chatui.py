import streamlit as st
from ClaimData import getContext
from app import ClaimAssistant
#from hugchat import hugchat
#from hugchat.login import Login

# App title
st.set_page_config(page_title="Claim Assistant")
print("Starting app")
# Hugging Face Credentials
with st.sidebar:
    st.markdown('📖Learn more about your claims')
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():

    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]
    getContext()
    
    
    

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(question, email, passwd):
    mem_id="MEM1"
    ca=ClaimAssistant()
    collection=ca.getCollection()
    context=collection.query(query_texts=question, where={"member_id":mem_id},n_results=3)["documents"]
    
    prompt= f"Use the following context to answer the question at the end preciously. {context} Question: {question}"
    print(prompt)
    answer=ca.query(prompt)
    print(answer)
    return answer

# User-provided prompt
if prompt := st.chat_input("Enter your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, "dummy", "dummt") 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
