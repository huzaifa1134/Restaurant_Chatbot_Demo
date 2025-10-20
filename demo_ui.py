import streamlit as st
import requests
import json


# Backend Server ADdress
API_BASE_URL = "http://127.0.0.1:8000"

# LEAD CAPTURE LOGIC
def save_lead(name: str, phone: str, initial_message: str) -> bool:
    
    lead_data = {
        "name": name,
        "phone": phone,
        "message": initial_message  # User ka pehla message as Lead message save hoga
    }
    try:
        response = requests.post(f"{API_BASE_URL}/crm/leads", json=lead_data, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        # Agar server down ho ya error ho, toh Streamlit ko bata dein
        st.error(f"Lead cannot be saved, Error: {e}")
        return False

# CHAT LOGIC 
def get_gemini_response(message: str) -> str:
    """
    Backend ke /gemini/chat endpoint se jawab laata hai.
    """
    try:
        # /gemini/chat route ko call karna
        response = requests.post(
            f"{API_BASE_URL}/gemini/chat",
            json={"message": message}
        )
        response.raise_for_status()
        return response.json().get("reply", "Sorry for Inconvinience.")
    except Exception as e:
        return f"Connection from Backend has been broken: {e}"

# --- 4. STREAMLIT APP UI ---
st.set_page_config(page_title="Restaurant Chatbot Demo", layout="centered")

# Session State ko check karna ke Lead capture ho chuki hai ya nahi
if "lead_captured" not in st.session_state:
    st.session_state["lead_captured"] = False
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- LEAD FORM ---
if not st.session_state["lead_captured"]:
    st.title("Welcome to Restaurant Chatbot Demo")
    st.markdown("**(This is a Demo Version of Chatbot as a Restaurant Assistant and Customer Support)**")

    with st.form("lead_form"):
        name = st.text_input("Your Name:", key="name")
        phone = st.text_input("Phone Number:", key="phone")
        first_message = st.text_area("Message:", key="initial_msg")
        
        submitted = st.form_submit_button("Chat with Bot")

        if submitted:
            if name and phone and first_message:
                if save_lead(name, phone, first_message):
                    # Lead save hone ke baad state update, aur pehla message chat history mein jayga
                    st.session_state["lead_captured"] = True
                    st.session_state["messages"].append({"role": "user", "content": first_message})
                    with st.spinner("..."):
                    # Existing function ko call karna
                      initial_reply = get_gemini_response(first_message) 
                
                # 2. Assistant ka Jawab History mein Add karna
                    st.session_state["messages"].append({"role": "assistant", "content": initial_reply}) 
                    st.rerun() # Page refresh
                else:
                    st.error("Lead cannot be saved please check the server.")
            else:
                st.warning("kindly Enter Name, Phone Number and your Message.")

# --- CHAT INTERFACE ---
else:
    st.title("🤖 Restaurant Assistant")

    # Purane messages ko display karna
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Naya message input
    if prompt := st.chat_input("Enter you Query..."):
        # User ka message history mein add karna
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gemini se jawab laana
        with st.spinner("Assistant is thinking Please wait..."):
            # Yahan hum /gemini/chat ko naya message bhej rahe hain
            response = get_gemini_response(prompt)
        
        # Assistant ka jawab history mein add karna
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})