import streamlit as st

import rag_helper
import video_helper

if "current_video_url" not in st.session_state:
    st.session_state.current_video_url = None
    st.session_state.current_transcrypt_docs = []
    st.session_state.videos = []
    

st.set_page_config(
    page_title="ChatWithVideo: Chat With Youtube Videos", layout="centered"
)
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
                video_transcrypted_docs = video_helper.get_video_transcrypt(
                    url=video_url
                )
                st.session_state.current_transcrypt_docs = video_transcrypted_docs
        st.success("Video transcrypted and cached!")
        st.divider()
        st.session_state.current_video_url = video_url
        

        with st.spinner("Your questions is responding..."):
            AI_response, relevant_documents= rag_helper.rag_with_video_transcrypt(
                transcrypted_docs=st.session_state.current_transcrypt_docs, prompt=promt
            )
        st.info("Response:")
        st.markdown(AI_response)
        st.divider()
        
        for doc in relevant_documents:
            st.warning("Reference:")
            st.caption(doc.page_content)
            st.markdown(f"Source: {doc.metadata}")
            st.divider()
            
with tab_search:
    col_left, col_center, col_right = st.columns([20,1,10])
    
    with col_left:
        st.subheader("Video search steps")
        st.divider()
        search_term = st.text_input(label="Enter search words:", key="search_term")
        video_count = st.slider(label="Result count", min_value=1, max_value=5)
        sorting_options = ["Relevance","Date","Views","Likes"]
        sorting_criteria = st.selectbox(label="Sorting criteria",options=sorting_options)
        search_btn = st.button(label="Search Video", key="search_btn")
        st.divider()
        
        if search_btn:
            st.session_state.video = []
            with st.spinner("Searching videos..."):
                video_list = video_helper.get_videos_for_search_term(
                    search_term=search_term, video_count=video_count, sorting_criteria=sorting_criteria
                )
            for video in video_list:
                st.session_state.videos.append(video)
            
        video_urls = []
        video_titles = {}
        for video in st.session_state.videos:
            video_urls.append(video.video_url)
            video_titles.update({video.video_url: video.video_title})
            

        selected_video = st.selectbox(
            label= "Choose video to chat with",
            options= video_urls,
            format_func=lambda url: video_titles[url],
            key= "search_selectbox"
        )
            
        if selected_video:
            search_prompt = st.text_input(label="Enter your question:", key="search_prompt2")
            search_ask_btn = st.button(label="Ask", key="search_ask_btn")
            
            if search_ask_btn:
                
                st.caption("Selected video")
                st.video(data=selected_video)
                st.divider()
                
                if st.session_state.current_video_url != selected_video:
                    with st.spinner("Transcrypting video..."):
                        video_transcrypted_docs = video_helper.get_video_transcrypt(
                            url=selected_video
                        )
                    st.session_state.current_transcrypt_docs = video_transcrypted_docs
                    st.success("Video transcrypted and cached!")
                    st.divider()
                    st.session_state.current_video_url = selected_video
        

                with st.spinner("Your questions is responding..."):
                    AI_response, relevant_documents= rag_helper.rag_with_video_transcrypt(
                        transcrypted_docs=st.session_state.current_transcrypt_docs, prompt=search_prompt
                    )
                st.info("Response:")
                st.markdown(AI_response)
                st.divider()
            
                for doc in relevant_documents:
                    st.warning("Reference:")
                    st.caption(doc.page_content)
                    st.markdown(f"Source: {doc.metadata}")
                    st.divider()

    
    with col_center:
        st.empty()

    with col_right:
        st.subheader("Related Videos")
        st.divider()
        
        for i, video in enumerate(st.session_state.videos):
            st.info(f"video Number:{i+1}")
            st.video(data=video.video_url)
            st.caption(f"Title:{video.video_title}")
            st.caption(f"Channel:{video.channel_name}")
            st.caption(f"Duration:{video.duration}")
            st.divider()
            
            
                               
        
    