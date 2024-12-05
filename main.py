import streamlit as st
import openai

st.title("Echo Bot")

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize the model to be used
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What's up?"):
    
    # Display the user's message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user's message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Initialize assistant's response display with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Placeholder for streaming response
        full_response = ""

        # Prepare the conversation history
        conversation_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        # Stream the response from OpenAI API using completions.create() for OpenAI v1.0.0 or higher
        for response in openai.completions.create(
            model=st.session_state["openai_model"],
            messages=conversation_history,
            stream=True
        ):
            # Update full response by appending the streaming content
            full_response += response['choices'][0].get('delta', {}).get('content', '')
            message_placeholder.markdown(full_response + "|")  # Show the streaming response
        
        # Once streaming is finished, display the complete response
        message_placeholder.markdown(full_response)

    # Add assistant's full response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
