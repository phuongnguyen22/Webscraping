import streamlit as st
import pandas as pd
import base64
from data_info.scrape_info import get_all_product_info

# Display the logo
st.image("image/picture1.png", width=300) # Adjust the width as needed
st.title("Scrape information desired from the website")
st.write("Give your URL, select the target information then click the button to get it.")


st.write(' ')
st.write(' ')
st.write(' ')


# Input the base_URL
base_url = "https://www.fossil.com"

# Input box for URL
url = st.text_input('Give your URL')

# Define the options
options = ['Name', 'ID', 'Brand', 'Gender', 'State', 'Price', 'Category']

# Use multiselect to allow the user to select multiple options
selected_options = st.multiselect('Which information you need to scrape?', options)

# Join the selected options into a single string
selected_options_str = ', '.join(selected_options)

# Display the selected options
st.write(f"You selected: {selected_options_str}")

# Button to run web scraping function
if st.button('Click'):
    #st.write(url)
    result = get_all_product_info(base_url, url)
    st.write(result)

    # Convert the result in a dataframe
    df = pd.DataFrame(result)
    if 'Price' in df.columns:
        df['Price'] = df['Price'].str.replace("â‚¬", "€")

    # Create a CSV download link
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode()).decode() # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="product_info.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)