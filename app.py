import os
import requests
import replicate
import streamlit as st
from dotenv import load_dotenv
# export REPLICATE_API_TOKEN="your_replicate_token"
# .env file w/  REPLICATE_API_TOKEN="your_replicate_token"
load_dotenv()

Llama2_7B       = "meta/llama-2-7b-chat:f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4"
Llama2_13B      = "meta/llama-2-13b-chat:56acad22679f6b95d6e45c78309a2b50a670d5ed29a37dd73d182e89772c02f1"
Llama2_70B      = "meta/llama-2-70b-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48"
Mixtral_8x7b    = "mistralai/mixtral-8x7b-instruct-v0.1:cf18decbf51c27fed6bbdc3492312c1c903222a56e3fe9ca02d6cbe5198afc10"
Replit_Code_3B  = "replit/replit-code-v1-3b:b84f4c074b807211cd75e3e8b1589b6399052125b4c27106e43d47189e8415ad"

MIN_TOKENS = 32
DEF_TOKENS = 120
MAX_TOKENS = 128

REPLICATE_URL = "https://api.replicate.com/v1/models/"

st.set_page_config(page_title="🧠 knoxBot")

def is_token_valid(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Token is valid")
        return True
    else:
        print("Token is invalid")
        return False

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_response(prompt, model, token):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    headers = {"Authorization": f"Bearer {token}"}
    output_generator = replicate.run(
        model,
        input={
            "prompt": f"{string_dialogue} {prompt} Assistant: ",
            "top_p": st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01),
            "max_length": st.sidebar.slider('max_length', min_value=MIN_TOKENS, max_value=MAX_TOKENS, value=DEF_TOKENS, step=8),
            "temperature": st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01),
            "repetition_penalty": 1
        }
    )
    output = list(output_generator)
    return output

# Function to print response dynamically
def live_update_response(response):
    placeholder = st.empty()
    full_response = ''
    for item in response:
        full_response += item
        placeholder.markdown(full_response)
    return full_response

# Start of Sidebar  ################################################################
with st.sidebar:
    st.title('🧠 knoxBot')
    st.write('This chatbot is created using the open-source models hosted on Replicate.')
    st.subheader('Models and parameters')
    models = {
        "Llama2-7B": Llama2_7B,
        "Llama2-13B": Llama2_13B,
        "Llama2-70B": Llama2_70B
    }
    model_name = st.sidebar.selectbox(
        'Choose a model', 
        list(models.keys()),
        key='model'
    )
    model = models[model_name]
    # model_url = REPLICATE_URL + model

    if os.getenv('REPLICATE_API_TOKEN'):
        st.success('API key already provided !', icon='✅')
        replicate_api_token = os.getenv('REPLICATE_API_TOKEN')
    else:
        replicate_api_token = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api_token.startswith('r8_') and len(replicate_api_token)==40):
            st.warning('Please enter your credentials !', icon='⚠️')
        else:
            st.success('Proceed w/ your prompt !', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api_token
# End  of  Sidebar  ################################################################

# Start of Mainpage ################################################################
if not replicate_api_token:
    st.error('No API token provided. Please enter your API token.')
    st.stop()

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User prompt as input
if prompt := st.chat_input(disabled=not replicate_api_token):
    if prompt.strip():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking ..."):
                    print(f">> Prompt: {prompt}\n")
                    print(f">> Token : {replicate_api_token}\n")
                    response = generate_response(prompt, model, replicate_api_token)
                    full_response = live_update_response(response)
                    # st.write(response)                        # delayed response
            print(f">> Output : {full_response}\n")
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)

    else:
        st.warning("Please enter a prompt.")
# End  of  Mainpage ################################################################


# HF model locally hosted
# from transformers import AutoModelForCausalLM, AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained(model)
# model = AutoModelForCausalLM.from_pretrained(model)

