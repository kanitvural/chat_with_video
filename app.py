import streamlit as st
import video_helper, rag_helper

if "current_video_url" not in st.session_state:
    st.session_state.current_video_url = None
    st.session_state.current_transcrypt_docs = []

st.set_page_config(page_title="ChatWithVideo: Chat With Youtube Videos", layout="centered")
st.image("./img/banner.webp")
st.title("ChatWithVideo: Chat With Youtube Videos")
st.divider()

tab_url, tab_search = st.tabs(["With URL", "With Search"])

with tab_url:
    
    
    video_url = st.text_input(label="Enter Youtube Video URL:", key="url_video")
    promt = st.text_input(label="Enter Your Question:", key="url_question")
    submit_btn = st.button(label="Ask", key="url_submit") 
    
    
    if submit_btn:
        st.video(data=video_url)
        st.divider()
        if st.session_state.current_video_url != video_url:
            with st.spinner("Transcrypting video..."):
                video_transcrypted_docs = video_helper.get_video_transcrypt(url=video_url) 
        st.success("Video Transcrypted and cached!")
        st.divider()
        st.session_state.current_video_url = video_url
        st.session_state.current_transcrypt_docs = video_transcrypted_docs

        
       
    

