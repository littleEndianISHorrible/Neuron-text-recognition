import streamlit as st

st.title('document recognition tool')
st.subheader('you can download your file to recognize text in it, then you will get a dataframe that will be show below')
uploaded_file = st.file_uploader('choise a *.pdf-file', type='pdf')  # optional
if uploaded_file is not None and uploaded_file.name.endswith('.pdf'):  # check if file is not none and it is a pdf file.
	st.write("I've got a file!")
else:
	st.write("I've got nothing to working with!")  # if file is not a pdf file, show a message

# add a button to run script src/backend/recognition.py
if st.button('run'):
	st.write('running...')

# TODO add a function auto show the recognition result
# TODO  add button to download the result of the script into database


# To run this:
# in power shell:
# streamlit run stlit.py
