import streamlit as st
import json

# Dummy in-memory database to store shopkeeper credentials and items
if 'shopkeepers' not in st.session_state:
    st.session_state.shopkeepers = {}

# Helper function to save shopkeeper credentials and items
def save_shopkeeper_data(shopkeepers):
    st.session_state.shopkeepers = shopkeepers

# Shopkeeper sign-up function
def sign_up():
    st.subheader("Sign Up")
    shopkeeper_id = st.text_input("Set your Shopkeeper ID", key="signup_id")
    password = st.text_input("Set your Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if shopkeeper_id in st.session_state.shopkeepers:
            st.error("Shopkeeper ID already exists. Please choose a different one.")
        else:
            st.session_state.shopkeepers[shopkeeper_id] = {
                'password': password,
                'items': []
            }
            save_shopkeeper_data(st.session_state.shopkeepers)
            st.success("Sign-up successful! You can now sign in.")

# Shopkeeper sign-in function
def sign_in():
    st.subheader("Sign In")
    shopkeeper_id = st.text_input("Enter Shopkeeper ID", key="signin_id")
    password = st.text_input("Enter Password", type="password", key="signin_password")

    if st.button("Sign In"):
        if shopkeeper_id in st.session_state.shopkeepers:
            if st.session_state.shopkeepers[shopkeeper_id]['password'] == password:
                st.session_state.shopkeeper_logged_in = shopkeeper_id
                st.success(f"Welcome back, {shopkeeper_id}!")
            else:
                st.error("Invalid password.")
        else:
            st.error("Invalid Shopkeeper ID.")

# Shopkeeper's item management
def manage_items():
    st.subheader("Manage Your Items")

    if 'shopkeeper_logged_in' in st.session_state:
        shopkeeper_id = st.session_state.shopkeeper_logged_in
        items = st.session_state.shopkeepers[shopkeeper_id]['items']

        item_name = st.text_input("Enter Item Name")
        item_rate = st.text_input("Enter Item Rate")
        item_image = st.file_uploader("Upload Item Image (optional)", type=["png", "jpg", "jpeg"])

        if st.button("Add/Update Item"):
            if item_name and item_rate:
                item_data = {'name': item_name, 'rate': item_rate, 'image': item_image}
                items.append(item_data)
                st.session_state.shopkeepers[shopkeeper_id]['items'] = items
                save_shopkeeper_data(st.session_state.shopkeepers)
                st.success("Item added/updated successfully!")
            else:
                st.error("Please provide both item name and rate.")

        # Display added items
        if items:
            st.subheader("Your Items")
            for item in items:
                st.write(f"Item: {item['name']}, Rate: {item['rate']}")
                if item['image']:
                    st.image(item['image'], caption=item['name'], use_column_width=True)
        else:
            st.write("No items added yet.")

# Customer search function
def customer_search():
    st.subheader("Customer Search")
    search_option = st.radio("Search by", ("Shopkeeper ID", "Item Name"))

    if search_option == "Shopkeeper ID":
        shopkeeper_id = st.text_input("Enter Shopkeeper ID to view items")
        if st.button("Search"):
            if shopkeeper_id in st.session_state.shopkeepers:
                items = st.session_state.shopkeepers[shopkeeper_id]['items']
                if items:
                    st.subheader(f"Items by {shopkeeper_id}")
                    for item in items:
                        st.write(f"Item: {item['name']}, Rate: {item['rate']}")
                        if item['image']:
                            st.image(item['image'], caption=item['name'], use_column_width=True)
                else:
                    st.write("No items available.")
            else:
                st.error("Invalid Shopkeeper ID.")

    elif search_option == "Item Name":
        item_name = st.text_input("Enter Item Name to search")
        if st.button("Search"):
            found = False
            for shopkeeper_id, data in st.session_state.shopkeepers.items():
                items = data['items']
                for item in items:
                    if item['name'].lower() == item_name.lower():
                        st.subheader(f"Found in {shopkeeper_id}'s store")
                        st.write(f"Item: {item['name']}, Rate: {item['rate']}")
                        if item['image']:
                            st.image(item['image'], caption=item['name'], use_column_width=True)
                        found = True
            if not found:
                st.write("No shopkeepers have this item.")

# Streamlit app
st.title("Superstore Application")

# Sidebar for selecting mode
mode = st.sidebar.selectbox("Choose Mode", ["Customer", "Shopkeeper"])

# Shopkeeper mode: Sign up, sign in, and manage items
if mode == "Shopkeeper":
    if 'shopkeeper_logged_in' not in st.session_state:
        sign_up()
        st.write("Already have an account? Sign in below:")
        sign_in()
    else:
        manage_items()

# Customer mode: Search for items by shopkeeper or item name
elif mode == "Customer":
    customer_search()
