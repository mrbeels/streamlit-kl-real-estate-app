import streamlit as st
import numpy as np
import webbrowser
import pickle
import json

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

### Header and SubHeader
st.write("""
# KL Real Estate Price Prediction
""")

st.write("""
### Deployed by Mr Beels
""")

# Github Button
url = "https://github.com/mrbeels"


def github_link():
    webbrowser.open(url)


if st.button('Github'):
    github_link()

# Location selector

with open('artifacts/columns.json') as f:
    data = json.load(f)

# Obtain inputs
data_columns = data['data_columns']
location_list = data['data_columns'][3:]

location = st.selectbox("Location", (location_list))

size = st.slider(label="Square Feet", min_value=325, max_value=39000)

rooms = st.slider(label="Rooms", min_value=1, max_value=20)

bathrooms = st.slider(label="Bathrooms", min_value=1, max_value=20)

# Predict

# Load Decision Tree Regressor Model
model = pickle.load(open('artifacts/kl_real_estate_dtr.pickle', 'rb'))


def price_predict(location, size, bathrooms, rooms):
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = size
    x[1] = bathrooms
    x[2] = rooms
    if loc_index >= 0:
        x[loc_index] = 1

    return int(model.predict([x])[0])


if st.button('Predict'):
    prediction = price_predict(location, size, bathrooms, rooms)
    st.balloons()
    st.success(
        f'Price of a {size:,} sqft {rooms} room & {bathrooms} bathroom property in {location.title()} is RM{prediction:,}.')
