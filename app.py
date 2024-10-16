import streamlit as st
import streamlit_authenticator as stauth
from google.oauth2 import id_token
from google.auth.transport import requests
from transformers import pipeline
import pandas as pd
import json

# Google OAuth configuration
CLIENT_ID = 'your-google-client-id.apps.googleusercontent.com'

# Dummy Hugging Face model for demo
# Use a pipeline as a high-level helper
from transformers import pipeline

hf_model = pipeline("text-generation", model="shahidul034/text_generation_bangla_model")
#hf_model = pipeline("text-generation", model="gpt2")

# Dummy database to store shopkeeper items (can be extended with a proper database)
shopkeeper_data = {}

# Function to verify Google OAuth sign-in
def verify_google_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        return idinfo
    except ValueError:
        return None

# Streamlit app begins
st.title("Superstore Application")

# Choose user mode
mode = st.sidebar.selectbox("Choose Mode", ["Customer", "Shopkeeper"])

# Shopkeeper Mode
if mode == "Shopkeeper":
    st.header("Shopkeeper Mode")
    
    # Sign up/sign in for shopkeeper (using Google OAuth)
    if 'logged_in' not in st.session_state:
        email = st.text_input("Enter your Gmail account")
        google_token = st.text_input("Enter your Google token for authentication")
        
        if st.button("Sign In"):
            user_info = verify_google_token(google_token)
            if user_info and user_info['email'] == email:
                st.session_state.logged_in = True
                st.success(f"Welcome, {user_info['name']}!")
            else:
                st.error("Invalid Google credentials.")

    # After successful login
    if st.session_state.get('logged_in', False):
        st.write("You are logged in as a Shopkeeper.")

        # Upload item data (images and rates)
        uploaded_files = st.file_uploader("Upload Item Images", type=["png", "jpg"], accept_multiple_files=True)
        item_names = st.text_area("Enter Item Names (comma separated)")
        item_rates = st.text_area("Enter Item Rates (comma separated)")

        if st.button("Submit Items"):
            if uploaded_files and item_names and item_rates:
                names = item_names.split(',')
                rates = item_rates.split(',')
                
                for i, file in enumerate(uploaded_files):
                    item_data = {
                        'name': names[i].strip(),
                        'rate': rates[i].strip(),
                        'image': file
                    }
                    shopkeeper_data[f"item_{i}"] = item_data
                
                st.success("Items uploaded successfully!")
            else:
                st.error("Please upload all details.")

        # Display items uploaded
        if shopkeeper_data:
            st.subheader("Your Uploaded Items")
            data = [{"Item": v['name'], "Rate": v['rate']} for k, v in shopkeeper_data.items()]
            df = pd.DataFrame(data)
            st.table(df)

# Customer Mode
elif mode == "Customer":
    st.header("Customer Mode")
    
    # Browse and order items uploaded by shopkeeper
    if shopkeeper_data:
        st.subheader("Available Items")
        for key, item in shopkeeper_data.items():
            st.image(item['image'], caption=item['name'])
            st.write(f"Price: {item['rate']}")
            if st.button(f"Order {item['name']}", key=key):
                st.success(f"You have ordered {item['name']}!")
    else:
        st.write("No items available at the moment.")
