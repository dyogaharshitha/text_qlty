import streamlit as st
import txt_qlty


def main():
    st.title("Get quality of article")

    # Define a number input widget
    url1 = st.text_input("Type Url of wikipedia page:",  value='https://en.wikipedia.org/wiki/February_29')
    para = None

    if st.checkbox('Type your own paragraph'):
        para = st.text_input("paragraph : ", value='start here...') ;
        url1 = None

    # Define a submit button
    submit_button = st.button("Submit")

    # Check if the submit button is pressed
    if submit_button:
        rw, cont = txt_qlty.get_scores(url1,para)

        # Display the output
        st.write("Content score :", rw)
        st.write("your content :", cont)


if __name__ == "__main__":
    main()
