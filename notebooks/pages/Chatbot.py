import streamlit as st
import google.generativeai as ggi

# Load the API key from secrets
api_key = st.secrets["GEMINI_API_KEY"]
ggi.configure(api_key=api_key)

with open('D:/Downloads/final-year-project/notebooks/stylesheets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize the generative model and chat
model = ggi.GenerativeModel("gemini-pro") 
chat = model.start_chat()

# Function to get response from LLM
def LLM_Response(question):
    response = chat.send_message(question, stream=True)
    return "".join([word.text for word in response])

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit app layout
st.markdown("<p class='custom-chatbot-title'>Chat Application using Gemini Pro</p>", unsafe_allow_html=True)

# Move the rainbow to the left
st.markdown(
    """
    <div class='rainbow' style='margin-bottom: 2rem; text-align: left;'>
        <!-- Your rainbow content here -->
    </div>
    """,
    unsafe_allow_html=True
)

# Suggested questions
st.info("""
**Here are some common questions you can ask:**
""")

quest1 = "What is building energy demand forecasting? Please explain in 3 sentences."
quest2 = "State 3 Importances of forecast energy demand in buildings."
quest3 = "Provide 3 Reasons why energy demand forecasting help the energy suppliers."

def update_conversation_history(quest):
    # Get response from LLM
    result = LLM_Response(quest)

    # Append user question and LLM response to conversation
    st.session_state.messages.append({"role": "user", "content": quest})
    st.session_state.messages.append({"role": "assistant", "content": result})

    # Rerun to update the conversation history
    st.experimental_rerun()

# Handle button click
if st.button(quest1):
    update_conversation_history(quest1)
if st.button(quest2):
    update_conversation_history(quest2)
if st.button(quest3):
    update_conversation_history(quest3)

# Display conversation history
for message in st.session_state.messages:
    message["content"] = message["content"].replace("\n\n","<br /><br />\n")
    if message["role"] == "user":
        st.markdown(f'<p class="user-msg">User: {message["content"]}</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="bot-msg">Gemini:<br />\n{message["content"]}</p>', unsafe_allow_html=True)

# Input area for user question
user_quest = st.text_input("", key="input", placeholder="Type your message here...")

if st.button("Send") and user_quest:
    update_conversation_history(user_quest)
