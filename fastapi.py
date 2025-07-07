import streamlit as st

st.title("TASK PLANNER")

uploaded_file = st.file_uploader("Choose a file")
description = st.text_input("Enter description")

if uploaded_file and description:
    if st.button("Upload"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        data = {"description": description}
        response = requests.post("http://127.0.0.1:8000/upload/", files=files, data=data)

        st.write("Response from API:", response.json())
